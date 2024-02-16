"""
    Doc helper class for loader doc related task
"""
import ast
import os.path
from datetime import datetime
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import AiDataModel, AiDocs, ReportModel, Snippets, Summary, DataSource, LoadHistory
from pebblo.app.utils.utils import read_json_file, get_full_path
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.topic_classifier.topic_classifier import TopicClassifier
from pebblo.app.enums.enums import ReportConstants, CacheDir

# Init topic classifier
topic_classifier_obj = TopicClassifier()


class LoaderHelper:
    def __init__(self, app_details, data, load_id):
        self.app_details = app_details
        self.data = data
        self.load_id = load_id
        self.loader_mapper = {}
        self.entity_classifier_obj = EntityClassifier()

    # Initialization
    def _initialize_raw_data(self):
        """
            Initializing raw data and return as dict object
        """
        if "report_metadata" in self.app_details.keys():
            return self.app_details['report_metadata']

        raw_data = {"total_findings": 0, "findings_entities": 0, "findings_topics": 0,
                    "data_source_count": 1, "data_source_snippets": list(),
                    "loader_source_snippets": {}, "file_count": 0,
                    "snippet_count": 0, "data_source_findings": {},
                    "snippet_counter": 0, "total_snippet_counter": 0}
        return raw_data

    @staticmethod
    def _fetch_variables(raw_data):
        """
            Return list of variable's
        """
        # Initializing variables
        return (
            raw_data.get("loader_source_snippets"),
            raw_data.get("total_findings"),
            raw_data.get("findings_entities"),
            raw_data.get("findings_topics"),
            raw_data.get("snippet_count"),
            raw_data.get("file_count"),
            raw_data.get("data_source_findings")
        )

    @staticmethod
    def _update_raw_data(raw_data, loader_source_snippets, total_findings, findings_entities, findings_topics,
                         snippet_count, file_count, data_source_findings):
        """
            Reassigning raw data
        """
        raw_data.update({
            "loader_source_snippets": loader_source_snippets,
            "total_findings": total_findings,
            "findings_entities": findings_entities,
            "findings_topics": findings_topics,
            "snippet_count": snippet_count,
            "file_count": file_count,
            "data_source_findings": data_source_findings
        })

    # Model Creation
    def _create_doc_model(self, doc, doc_info):
        """
            Create doc model and return its object
        """
        loader_details = self.data.get("loader_details", {})
        last_used = datetime.now()
        doc_model = AiDocs(appId=self.load_id,
                           doc=doc.get('doc'),
                           sourceSize=doc.get('source_path_size', 0),
                           fileOwner=doc.get('file_owner', '-'),
                           sourcePath=doc.get('source_path'),
                           loaderSourcePath=loader_details.get("source_path"),
                           lastModified=last_used,
                           entityCount=doc_info.entityCount,
                           entities=doc_info.entities,
                           topicCount=doc_info.topicCount,
                           topics=doc_info.topics)
        return doc_model.dict()

    @staticmethod
    def _get_top_n_findings(raw_data):
        """
            Return top N findings from all findings
        """
        logger.debug("Getting top N findings details and aggregate them")
        loader_source_snippets = raw_data["loader_source_snippets"]
        top_n_findings_list = sorted(loader_source_snippets.items(), key=lambda x: x[1]['findings'], reverse=True)[
                              :ReportConstants.top_findings_limit.value]
        top_n_findings = [
            {
                "fileName": key,
                "fileOwner": "-" if value.get("fileOwner", "-") is None else value.get("fileOwner", "-"),
                "sourceSize": 0 if value.get("sourceSize", 0) is None else value.get("sourceSize", 0),
                "findingsEntities": value['findings_entities'],
                "findingsTopics": value['findings_topics'],
                "findings": value['findings']
            }
            for key, value in top_n_findings_list
        ]
        return top_n_findings

    def _count_files_with_findings(self):
        """
            Return the count of files that have associated findings.
        """
        logger.debug("Fetching the count of files that have associated findings")
        files_with_findings_count = 0
        loader_details = self.app_details.get("loaders", {})
        for loader in loader_details:
            for file_dict in loader["sourceFiles"]:
                if "findings" in file_dict.keys() and file_dict["findings"] > 0:
                        files_with_findings_count += 1
        return files_with_findings_count

    def _get_classifier_response(self, doc):
        doc_info = AiDataModel(data=doc.get("doc", None),
                               entities={}, entityCount=0,
                               topics={}, topicCount=0)
        try:
            if doc_info.data:
                topics, topic_count = topic_classifier_obj.predict(doc_info.data)
                entities, entity_count = self.entity_classifier_obj.presidio_entity_classifier(doc_info.data)
                secrets, secret_count = self.entity_classifier_obj.presidio_secret_classifier(doc_info.data)
                entities.update(secrets)
                entity_count += secret_count
                doc_info.topics = topics
                doc_info.entities = entities
                doc_info.topicCount = topic_count
                doc_info.entityCount = entity_count
            return doc_info
        except Exception as e:
            logger.error(f"Get Classifier Response Failed, Exception: {e}")
            return doc_info

    def _update_app_details(self, raw_data, ai_app_docs):
        """
            Updating ai app details loader source files
        """
        logger.debug("Updating app details")
        self.app_details["docs"] = ai_app_docs
        loader_source_snippets = raw_data["loader_source_snippets"]
        # Updating app_details doc list and loader source files
        loader_details = self.app_details.get("loaders", {})
        for loader in loader_details:
            for source_file in loader.get("sourceFiles", []):
                name = source_file["name"]
                if name not in loader_source_snippets:
                    loader_source_snippets[name] = source_file

            new_source_files = [{
                    "name": key,
                    "findings_entities": value['findings_entities'],
                    "findings_topics": value['findings_topics'],
                    "findings": value['findings']
                }
                for key, value in loader_source_snippets.items()
            ]

            loader["sourceFiles"] = new_source_files
        self.app_details["report_metadata"] = raw_data

    @staticmethod
    def _get_finding_details(doc, data_source_findings, entity_type, raw_data):
        """
            Retrieve finding details from data source
        """
        logger.debug(f"Fetching finding details from data source for entity type: {entity_type}")
        source_path = doc.get("sourcePath")
        snippet = Snippets(snippet=doc["doc"],
                           sourcePath=source_path,
                           fileOwner=doc.get("fileOwner", "-"))
        for label_name, value in doc[entity_type].items():
            if label_name in data_source_findings.keys():
                data_source_findings[label_name]["snippetCount"] += 1
                data_source_findings[label_name]["findings"] += value
                raw_data["total_snippet_counter"] += 1

                unique_snippets_set = data_source_findings[label_name]["unique_snippets"]
                if isinstance(unique_snippets_set, str):
                    # When we write data_source_findings[label_name]['unique_snippets'] to metadata file,
                    # it gets stored as str. We would need it as set again for further processing.
                    # This is why we are using as.literal_eval() here.
                    unique_snippets_set = ast.literal_eval(data_source_findings[label_name]['unique_snippets'])
                unique_snippets_set.add(source_path)
                data_source_findings[label_name]["fileCount"] = len(unique_snippets_set)
                data_source_findings[label_name]["unique_snippets"] = unique_snippets_set

                #  If the snippet count exceeds the snippet limit,
                #  we will refrain from adding the snippet to the snippet list
                if raw_data["snippet_counter"] < ReportConstants.snippets_limit.value:
                    data_source_findings[label_name]["snippets"].append(snippet.dict())
                    raw_data["snippet_counter"] += 1
            else:
                # The source path is encountered for the first time, so we are initializing its object.
                dict_obj = {
                    "labelName": label_name,
                    "findings": value,
                    "findingsType": entity_type,
                    "snippetCount": 1,
                    "fileCount": 1
                }
                data_source_findings[label_name] = dict_obj
                data_source_findings[label_name]["unique_snippets"] = set()
                data_source_findings[label_name]["unique_snippets"].add(source_path)
                raw_data["total_snippet_counter"] += 1

                #  If the snippet count exceeds the snippet limit,
                #  we will refrain from adding the snippet to the snippet list
                if raw_data["snippet_counter"] < ReportConstants.snippets_limit.value:
                    data_source_findings[label_name]["snippets"] = [snippet.dict()]
                    raw_data["snippet_counter"] += 1
                else:
                    data_source_findings[label_name]["snippets"] = []

    def _get_data_source_details(self, raw_data):
        """
            Create data source findings details and data source findings summary
        """
        logger.debug("Aggregating data source details")
        data_source_obj_list = list()
        for loader in self.app_details["loaders"]:
            name = loader.get("name")
            source_path = loader.get("sourcePath")
            source_type = loader.get("sourceType")
            source_size = loader.get("sourceSize")
            total_snippet_count = raw_data["total_snippet_counter"]
            displayed_snippet_count = raw_data["snippet_counter"]
            data_source_findings = [{key: value[key] for key in value if key != value[key] and key != "unique_snippets"}
                                    for value in
                                    raw_data["data_source_findings"].values()]

            # Create data source findings summary from data source findings
            data_source_findings_summary = self._create_data_source_findings_summary(data_source_findings)

            data_source_obj = DataSource(name=name,
                                         sourcePath=source_path,
                                         sourceType=source_type,
                                         sourceSize=source_size,
                                         totalSnippetCount=total_snippet_count,
                                         displayedSnippetCount=displayed_snippet_count,
                                         findingsSummary=data_source_findings_summary,
                                         findingsDetails=data_source_findings
                                         )
            data_source_obj_list.append(data_source_obj)
        return data_source_obj_list

    @staticmethod
    def _create_data_source_findings_summary(data_source_findings):
        """
            Creating data source findings summary and return it findings summary list
        """
        logger.debug("Creating data source summary")
        data_source_findings_summary = []
        for ds_findings in data_source_findings:
            label_name = ds_findings.get("labelName", "")
            findings = ds_findings.get("findings", 0)
            findings_type = ds_findings.get("findingsType")
            snippet_count = ds_findings.get("snippetCount", 0)
            file_count = ds_findings.get("fileCount", 0)

            data_source_findings_summary.append({
                "labelName": label_name,
                "findings": findings,
                "findingsType": findings_type,
                "snippetCount": snippet_count,
                "fileCount": file_count
            })

        return data_source_findings_summary

    def _create_report_summary(self, raw_data, files_with_findings_count):
        """
            Return report summary object
        """
        logger.debug("Creating report summary")
        report_summary = Summary(
            findings=raw_data["total_findings"],
            findingsEntities=raw_data["findings_entities"],
            findingsTopics=raw_data["findings_topics"],
            totalFiles=raw_data["file_count"],
            filesWithFindings=files_with_findings_count,
            dataSources=raw_data["data_source_count"],
            owner=self.app_details["owner"],
            createdAt=datetime.now()
        )
        return report_summary

    def _get_load_history(self):
        """
            Retrieve previous runs details and create load history and return
        """
        logger.debug("Fetching previous execution details and creating loader history")
        load_history = dict()
        # Reading metadata file & get load details
        app_name = self.data.get("name")
        current_load_id = self.load_id
        app_metadata_file_path = f"{CacheDir.home_dir.value}/{app_name}/{CacheDir.metadata_file_path.value}"
        app_metadata = read_json_file(app_metadata_file_path)
        if not app_metadata:
            # No app metadata is present
            return load_history
        load_ids = app_metadata.get("load_ids", [])

        # Retrieving load id report file
        # LoadHistory will be considered up to the specified load history limit.
        # if no of reports are greater than specified limit than, we provide the dir path for all reports
        load_history["history"] = list()
        load_history["moreReportsPath"] = "-"
        report_counts = len(load_ids)
        top_n_latest_loader_id = load_ids[-ReportConstants.loader_history_limit.value - 1:]
        top_n_latest_loader_id.reverse()

        for load_id in top_n_latest_loader_id:
            if load_id == current_load_id:
                continue
            load_report_file_path = f"{CacheDir.home_dir.value}/{app_name}/{load_id}/{CacheDir.report_data_file_name.value}"
            report = read_json_file(load_report_file_path)
            if report:
                pdf_report_path = f"{CacheDir.home_dir.value}/{app_name}/{load_id}/{CacheDir.report_file_name.value}"
                report_name = get_full_path(pdf_report_path)
                if not os.path.exists(report_name):
                    # Pdf file is not present, Skipping it
                    continue
                # create loader history object
                report_summary = report.get("reportSummary")
                load_history_model_obj = LoadHistory(loadId=load_id,
                                                     reportName=report_name,
                                                     findings=report_summary["findings"],
                                                     filesWithFindings=report_summary["filesWithFindings"],
                                                     generatedOn=report_summary["createdAt"]
                                                     )
                load_history["history"].append(load_history_model_obj.dict())
        if (len(load_history["history"]) == ReportConstants.loader_history_limit.value
                and report_counts > ReportConstants.loader_history_limit.value+1):
            more_reports = f"{CacheDir.home_dir.value}/{app_name}/"
            more_report_full_path = get_full_path(more_reports)
            load_history["moreReportsPath"] = more_report_full_path
        return load_history

    def _get_doc_report_metadata(self, doc, raw_data):
        """
            Retrieve metadata from the document, update the raw data, and then return the updated raw data.
        """
        logger.debug("fetching report data from input and aggregating data")
        # Initialize variables
        (loader_source_snippets, total_findings, findings_entities, findings_topics,
         snippet_count, file_count, data_source_findings) = self._fetch_variables(raw_data)
        # getting snippet details only if snippet has findings entities or topics.
        findings = doc["entityCount"] + doc["topicCount"]
        source_path = doc.get("sourcePath")

        # If source path is already present, then add values
        if source_path in loader_source_snippets.keys():
            loader_source_snippets[source_path]["findings_entities"] = (
                    loader_source_snippets[source_path].get("findings_entities", 0) + doc["entityCount"])
            loader_source_snippets[source_path]["findings_topics"] = (
                    loader_source_snippets[source_path].get("findings_topics", 0) + doc["topicCount"])
            loader_source_snippets[source_path]["findings"] += findings
            total_findings += findings
            findings_entities += doc["entityCount"]
            findings_topics += doc["topicCount"]
            snippet_count += 1

        # If source path is not present, then initialize values
        else:
            total_findings += findings
            loader_source_snippets[source_path] = {"findings_entities": doc["entityCount"],
                                                   "findings_topics": doc["topicCount"],
                                                   "findings": findings}
            findings_entities += doc["entityCount"]
            findings_topics += doc["topicCount"]
            snippet_count += 1
            file_count += 1
            loader_source_snippets[source_path]["fileOwner"] = doc["fileOwner"]
            loader_source_snippets[source_path]["sourceSize"] = doc['sourceSize']

        if len(doc["topics"]) > 0:
            self._get_finding_details(doc, data_source_findings, "topics", raw_data)
        if len(doc["entities"]) > 0:
            self._get_finding_details(doc, data_source_findings, "entities", raw_data)

        # Replace report_metadata
        self._update_raw_data(raw_data, loader_source_snippets, total_findings, findings_entities, findings_topics,
                              snippet_count, file_count, data_source_findings)
        return raw_data

    def _generate_final_report(self, raw_data):
        """
            Aggregating all input, processing the data, and generating the final report
        """
        logger.debug("Generating final report")

        # get count of files that have associated findings.
        files_with_findings_count = self._count_files_with_findings()

        # Create report summary
        report_summary = self._create_report_summary(raw_data, files_with_findings_count)

        # get top N findings
        top_n_findings = self._get_top_n_findings(raw_data)

        # Generating DataSource
        data_source_obj_list = self._get_data_source_details(raw_data)

        # Retrieve LoadHistory From previous executions
        load_history = self._get_load_history()

        report_dict = ReportModel(
            name=self.app_details["name"],
            description=self.app_details.get("description", "-"),
            instanceDetails=self.app_details["instanceDetails"],
            framework=self.app_details["framework"],
            reportSummary=report_summary,
            loadHistory=load_history,
            topFindings=top_n_findings,
            dataSources=data_source_obj_list
        )
        return report_dict.dict()

    def process_docs_and_generate_report(self):
        """
            Processing the doc and aggregate the report data
        """
        logger.debug("Processing docs and creating report data")
        # Initialize and load data
        input_doc_list = self.data.get('docs', [])
        ai_app_docs = self.app_details.get("docs", [])

        # Initialize raw data
        raw_data = self._initialize_raw_data()
        logger.debug("Iterating input doc list and perform classification and aggregating report data")
        for doc in input_doc_list:
            if doc:
                # Get classifier Response
                doc_info: AiDataModel = self._get_classifier_response(doc)
                doc_obj = self._create_doc_model(doc, doc_info)
                ai_app_docs.append(doc_obj)
                raw_data = self._get_doc_report_metadata(doc_obj, raw_data)

        # Updating ai apps details
        self._update_app_details(raw_data, ai_app_docs)

        # Generate Final Report
        final_report = self._generate_final_report(raw_data)
        return self.app_details, final_report
