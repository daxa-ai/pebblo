"""
    Doc helper class for loader doc related task
"""

from datetime import datetime
from analyzer.app.libs.logger import logger
from analyzer.app.models.models import Metadata, AiDataModel, AiDocs, ReportModel, Snippets, Summary, DataSource
from analyzer.entity_classifier.entity_classifier import EntityClassifier
from analyzer.topic_classifier.topic_classifier import TopicClassifier

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
                # secrets, secret_count = {}, 0
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

    def _get_finding_details(self, doc, data_source_findings, entity_type, file_count):
        source_path = doc.get("sourcePath")
        snippet = Snippets(snippet=doc["doc"],
                           sourcePath=source_path,
                           owner=doc.get("owner", " "),
                           size=doc.get("size", 0))
        for label_name, value in doc[entity_type].items():
            if label_name in data_source_findings.keys():
                data_source_findings[label_name]["labelName"] = label_name
                data_source_findings[label_name]["snippetCount"] += 1
                data_source_findings[label_name]["findings"] += value
                data_source_findings[label_name]["findingsType"] = entity_type
                data_source_findings[label_name]["snippets"].append(snippet.dict())
                unique_source_paths = set(snippet["sourcePath"]
                                          for snippet in data_source_findings[label_name]["snippets"])
                data_source_findings[label_name]["fileCount"] = len(unique_source_paths)
            else:
                dict_obj = {f"labelName": label_name, "findings": value, "findingsType": entity_type, "snippetCount": 1,
                            "fileCount": file_count}
                data_source_findings[label_name] = dict_obj
                data_source_findings[label_name]["snippets"] = [snippet.dict()]

    def _get_doc_report_metadata(self, doc, report_metadata_init):
        logger.debug("In Function: _get_doc_report_metadata")
        loader_source_snippets = report_metadata_init["loader_source_snippets"]
        total_findings = report_metadata_init["total_findings"]
        findings_entities = report_metadata_init["findings_entities"]
        findings_topics = report_metadata_init["findings_topics"]
        snippet_count = report_metadata_init["snippet_count"]
        file_count = report_metadata_init["file_count"]
        data_source_snippets = report_metadata_init["data_source_snippets"]
        data_source_findings = report_metadata_init["data_source_findings"]

        # getting snippet details only if snippet has restricted entities or topics.
        findings = doc["entityCount"] + doc["topicCount"]
        source_path = doc.get("sourcePath")
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
        else:
            total_findings += findings
            loader_source_snippets[source_path] = {"findings_entities": doc["entityCount"],
                                                   "findings_topics": doc["topicCount"],
                                                   "findings": total_findings}
            findings_entities += doc["entityCount"]
            findings_topics += doc["topicCount"]
            snippet_count += 1
            file_count += 1
            if source_path in self.loader_mapper.keys():
                loader_source_snippets[source_path]["owner"] = self.loader_mapper[source_path]["owner"]
                loader_source_snippets[source_path]["size"] = self.loader_mapper[source_path]["size"]

        if len(doc["topics"]) > 0:
            self._get_finding_details(doc, data_source_findings, "topics", file_count)
        if len(doc["entities"]) > 0:
            self._get_finding_details(doc, data_source_findings, "entities", file_count)

        report_metadata_init["loader_source_snippets"] = loader_source_snippets
        report_metadata_init["total_findings"] = total_findings
        report_metadata_init["findings_entities"] = findings_entities
        report_metadata_init["findings_topics"] = findings_topics
        report_metadata_init["snippet_count"] = snippet_count
        report_metadata_init["file_count"] = file_count
        report_metadata_init["data_source_snippets"] = data_source_snippets
        report_metadata_init["data_source_findings"] = data_source_findings
        return report_metadata_init

    def _get_data_source_details(self, report_metadata_init):
        data_source_obj_list = list()
        for loader in self.app_details["loaders"]:
            name = loader.get("name")
            source_path = loader.get("sourcePath")
            source_type = loader.get("sourceType")
            data_source_findings = [{key: value[key] for key in value if key != value[key]} for value in
                                    report_metadata_init["data_source_findings"].values()]
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
            data_source_obj = DataSource(name=name, sourcePath=source_path, sourceType=source_type,
                                         findingsSummary=data_source_findings_summary,
                                         findingsDetails=data_source_findings,
                                         snippets=report_metadata_init["data_source_snippets"])
            data_source_obj_list.append(data_source_obj)
        return data_source_obj_list

    def _generate_final_report(self, report_metadata_init):
        logger.debug("In Function: _generate_final_report")
        loader_source_snippets = report_metadata_init["loader_source_snippets"]
        file_count_restricted_data = 0
        for file_dict in self.app_details["loader_source_files"]:
            if "findings" in file_dict.keys():
                if file_dict["findings"] > 0:
                    file_count_restricted_data += 1

        report_summary = Summary(
            findings=report_metadata_init["total_findings"],
            findingsEntities=report_metadata_init["findings_entities"],
            findingsTopics=report_metadata_init["findings_topics"],
            totalFiles=report_metadata_init["file_count"],
            filesWithRestrictedData=file_count_restricted_data,
            dataSources=report_metadata_init["data_source_count"],
            owner=self.app_details["owner"]
        )

        # Get top N findings, currently 5
        top_n_findings = sorted(loader_source_snippets.items(), key=lambda x: x[1]['findings'], reverse=True)[:5]

        top_n_finding_objects = [
            {
                "fileName": key,
                "owner": "-" if value.get("owner", "-") is None else value.get("owner", "-"),
                "size": 0 if value.get("size", 0) is None else value.get("size", 0),
                "findingsEntities": value['findings_entities'],
                "findingsTopics": value['findings_topics'],
                "findings": value['findings']
            }
            for key, value in top_n_findings
        ]

        # Generating DataSource
        data_source_obj_list = self._get_data_source_details(report_metadata_init)
        report_dict = ReportModel(
            name=self.app_details["name"],
            description=self.app_details.get("description", " "),
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
        self.loader_mapper[loader_details.get("source_path")] = {"owner": loader_details.get("owner"),
                                                                 "size":loader_details.get("size"),
                                                                 "type": loader_details.get("source_type")}
        input_doc_list = self.data.get('docs', [])
        logger.debug("In Function: _get_doc_details_and_generate_report")
        metadata_obj = Metadata(createdAt=datetime.now(), modifiedAt=datetime.now())
        last_used = datetime.now()
        docs = self.app_details.get("docs", [])
        report_metadata_init = {"total_findings": 0, "findings_entities": 0, "findings_topics": 0,
                                "data_source_count": 1,
                                "data_source_snippets": list(), "loader_source_snippets": {}, "file_count": 0,
                                "snippet_count": 0, "data_source_findings": {}}
        loader_source_files = self.app_details.get("loader_source_files", [])
        for doc in input_doc_list:
            # Get classifier Response
            if doc:
                doc_info: AiDataModel = self._get_classifier_response(doc)
                doc_model = AiDocs(appId=self.load_id,
                                   metadata=metadata_obj,
                                   doc=doc.get('doc'),
                                   size=doc.get('size', 0),
                                   owner=doc.get('owner', '-'),
                                   sourcePath=doc.get('source_path'),
                                   loaderSourcePath=loader_details.get("source_path"),
                                   lastModified=last_used,
                                   entityCount=doc_info.entityCount,
                                   entities=doc_info.entities,
                                   topicCount=doc_info.topicCount,
                                   topics=doc_info.topics)
                docs.append(doc_model.dict())
                report_metadata_init = self._get_doc_report_metadata(doc_model.dict(), report_metadata_init)

        # Updating app_details doc list and loader source files
        loader_source_snippets = report_metadata_init["loader_source_snippets"]
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
        final_report = self._generate_final_report(report_metadata_init)
        return self.app_details, final_report
