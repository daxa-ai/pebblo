"""
    Doc helper class for loader doc related task
"""

from datetime import datetime
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import AiDataModel, AiDocs, ReportModel, Snippets, Summary, DataSource
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.topic_classifier.topic_classifier import TopicClassifier
from pebblo.app.enums.enums import ReportConstants

# Init topic classifier
topic_classifier_obj = TopicClassifier()
# Init topic classifier
entity_classifier_obj = EntityClassifier()


class DocHelper:
    def __init__(self, app_details, data, load_id):
        self.app_details = app_details
        self.data = data
        self.load_id = load_id
        self.loader_mapper = {}

    def _get_classifier_response(self, doc):
        doc_info = AiDataModel(data=doc.get("doc", None),
                               entities={}, entityCount=0,
                               topics={}, topicCount=0)
        try:
            if doc_info.data:
                topics, topic_count = topic_classifier_obj.predict(doc_info.data)
                entities, entity_count = entity_classifier_obj.presidio_entity_classifier(doc_info.data)
                secrets, secret_count = entity_classifier_obj.presidio_secret_classifier(doc_info.data)
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

    def _get_finding_details(self, doc, data_source_findings, entity_type, file_count, raw_data):
        source_path = doc.get("sourcePath")
        snippet = Snippets(snippet=doc["doc"],
                           sourcePath=source_path,
                           fileOwner=doc.get("fileOwner", " "))
        for label_name, value in doc[entity_type].items():
            if label_name in data_source_findings.keys():
                data_source_findings[label_name]["snippetCount"] += 1
                data_source_findings[label_name]["findings"] += value
                data_source_findings[label_name]["unique_snippets"].add(source_path)
                raw_data["total_snippet_counter"] += 1
                if raw_data["snippet_counter"] < ReportConstants.snippets_limit.value:
                    data_source_findings[label_name]["snippets"].append(snippet.dict())
                    raw_data["snippet_counter"] += 1
                data_source_findings[label_name]["fileCount"] = len(data_source_findings[label_name]["unique_snippets"])
            else:
                dict_obj = {f"labelName": label_name, "findings": value, "findingsType": entity_type, "snippetCount": 1,
                            "fileCount": file_count}
                data_source_findings[label_name] = dict_obj
                raw_data["total_snippet_counter"] += 1
                if raw_data["snippet_counter"] < ReportConstants.snippets_limit.value:
                    data_source_findings[label_name]["snippets"] = [snippet.dict()]
                    raw_data["snippet_counter"] += 1
                else:
                    data_source_findings[label_name]["snippets"] = []

                data_source_findings[label_name]["unique_snippets"] = set()
                data_source_findings[label_name]["unique_snippets"].add(source_path)

    def _get_doc_report_metadata(self, doc, raw_data):
        logger.debug("In Function: _get_doc_report_metadata")
        # Initialize variables
        loader_source_snippets = raw_data["loader_source_snippets"]
        total_findings = raw_data["total_findings"]
        findings_entities = raw_data["findings_entities"]
        findings_topics = raw_data["findings_topics"]
        snippet_count = raw_data["snippet_count"]
        file_count = raw_data["file_count"]
        data_source_findings = raw_data["data_source_findings"]

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
            self._get_finding_details(doc, data_source_findings, "topics", file_count, raw_data)
        if len(doc["entities"]) > 0:
            self._get_finding_details(doc, data_source_findings, "entities", file_count, raw_data)

        # Replace report_metadata
        raw_data["loader_source_snippets"] = loader_source_snippets
        raw_data["total_findings"] = total_findings
        raw_data["findings_entities"] = findings_entities
        raw_data["findings_topics"] = findings_topics
        raw_data["snippet_count"] = snippet_count
        raw_data["file_count"] = file_count
        raw_data["data_source_findings"] = data_source_findings
        return raw_data

    def _get_data_source_details(self, raw_data):
        data_source_obj_list = list()
        for loader in self.app_details["loaders"]:
            name = loader.get("name")
            source_path = loader.get("sourcePath")
            source_type = loader.get("sourceType")
            source_size = loader.get("sourceSize")
            total_snippet_count = raw_data["total_snippet_counter"]
            displayed_snippet_count = raw_data["snippet_counter"]
            data_source_findings = [{key: value[key] for key in value if key != value[key] and key != "unique_snippets"} for value in
                                    raw_data["data_source_findings"].values()]
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
            data_source_obj = DataSource(name=name,
                                         sourcePath=source_path,
                                         sourceType=source_type,
                                         sourceSize=source_size,
                                         totalSnippetCount = total_snippet_count,
                                         displayedSnippetCount = displayed_snippet_count,
                                         findingsSummary=data_source_findings_summary,
                                         findingsDetails=data_source_findings
                                         )
            data_source_obj_list.append(data_source_obj)
        return data_source_obj_list

    def _generate_final_report(self, raw_data):
        logger.debug("In Function: _generate_final_report")
        loader_source_snippets = raw_data["loader_source_snippets"]
        file_count_restricted_data = 0
        for file_dict in self.app_details["loader_source_files"]:
            if "findings" in file_dict.keys():
                if file_dict["findings"] > 0:
                    file_count_restricted_data += 1

        report_summary = Summary(
            findings=raw_data["total_findings"],
            findingsEntities=raw_data["findings_entities"],
            findingsTopics=raw_data["findings_topics"],
            totalFiles=raw_data["file_count"],
            filesWithRestrictedData=file_count_restricted_data,
            dataSources=raw_data["data_source_count"],
            owner=self.app_details["owner"]
        )

        # Get top N findings, currently 5
        top_n_findings = sorted(loader_source_snippets.items(), key=lambda x: x[1]['findings'], reverse=True)[:ReportConstants.top_findings_limit.value]
        top_n_finding_objects = [
            {
                "fileName": key,
                "fileOwner": "-" if value.get("fileOwner", "-") is None else value.get("fileOwner", "-"),
                "sourceSize": 0 if value.get("sourceSize", 0) is None else value.get("sourceSize", 0),
                "findingsEntities": value['findings_entities'],
                "findingsTopics": value['findings_topics'],
                "findings": value['findings']
            }
            for key, value in top_n_findings
        ]

        # Generating DataSource
        data_source_obj_list = self._get_data_source_details(raw_data)
        report_dict = ReportModel(
            name=self.app_details["name"],
            description=self.app_details.get("description", "-"),
            instanceDetails=self.app_details["instanceDetails"],
            framework=self.app_details["framework"],
            reportSummary=report_summary,
            topFindings=top_n_finding_objects,
            lastModified=datetime.now(),
            dataSources=data_source_obj_list
        )
        return report_dict.dict()

    def process_docs_and_generate_report(self):
        loader_details = self.data.get("loader_details", {})
        # should be list of loader obj
        self.loader_mapper[loader_details.get("source_path")] = {"fileOwner": self.data.get("source_owner"),
                                                                 "sourceSize": loader_details.get("source_size"),
                                                                 "type": loader_details.get("source_type")}
        input_doc_list = self.data.get('docs', [])
        logger.debug("In Function: _get_doc_details_and_generate_report")
        last_used = datetime.now()
        docs = self.app_details.get("docs", [])
        raw_data = {"total_findings": 0, "findings_entities": 0, "findings_topics": 0,
                                "data_source_count": 1,
                                "data_source_snippets": list(), "loader_source_snippets": {}, "file_count": 0,
                                "snippet_count": 0, "data_source_findings": {}, "snippet_counter": 0,
                                "total_snippet_counter": 0}
        loader_source_files = self.app_details.get("loader_source_files", [])
        for doc in input_doc_list:
            # Get classifier Response
            if doc:
                doc_info: AiDataModel = self._get_classifier_response(doc)
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
                docs.append(doc_model.dict())
                raw_data = self._get_doc_report_metadata(doc_model.dict(), raw_data)

        # Updating app_details doc list and loader source files
        loader_source_snippets = raw_data["loader_source_snippets"]
        self.app_details["docs"] = docs

        new_loader_source_files = [
            {
                "name": key,
                "findings_entities": value['findings_entities'],
                "findings_topics": value['findings_topics'],
                "findings": value['findings']
            }
            for key, value in loader_source_snippets.items()
        ]
        loader_source_files.extend(new_loader_source_files)
        self.app_details["loader_source_files"] = loader_source_files

        # Generate Final Report
        final_report = self._generate_final_report(raw_data)
        return self.app_details, final_report
