"""
    Copyright (c) 2024 Daxa. All rights reserved.
    Doc helper class for loader doc related task
"""

from datetime import datetime
from analyzer.app.libs.logger import logger
from analyzer.app.models.models import Metadata, AiDataModel, AiDocs, ReportModel, Snippets, Summary, DataSource
from analyzer.entity_classifier.entity_classifier import EntityClassifier
from analyzer.topic_classifier.topic_classifier import TopicClassifier

# Init topic classifier
topic_classifier_obj = TopicClassifier()


class DocHelper:
    def __init__(self, app_details, data, load_id):
        self.app_details = app_details
        self.data = data
        self.load_id = load_id

    def _get_classifier_response(self, doc):
        doc_info = AiDataModel(data=doc.get("doc", None),
                               entities={}, entityCount=0,
                               topics={}, topicCount=0)
        try:
            if doc_info.data:
                entity_classifier_obj = EntityClassifier(doc_info.data)
                topics, topic_count = topic_classifier_obj.predict(doc_info.data)
                entities, entity_count = entity_classifier_obj.presidio_entity_classifier()
                secrets, secret_count = entity_classifier_obj.presidio_secret_classifier()
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
        if entity_type == "entities":
            snippet = Snippets(snippet=doc["doc"],
                               sourcePath=source_path,
                               findings=doc["entityCount"],
                               findingType="entity")
        else:
            snippet = Snippets(snippet=doc["doc"],
                               sourcePath=source_path,
                               findings=doc["topicCount"],
                               findingType="topic")
        for label_name, value in doc[entity_type].items():
            if label_name in data_source_findings.keys():
                data_source_findings[label_name]["labelName"] = label_name
                data_source_findings[label_name]["snippetCount"] += 1
                data_source_findings[label_name]["fileCount"] += 1
                data_source_findings[label_name]["count"] += value
                data_source_findings[label_name]["snippets"].append(snippet.dict())
            else:
                dict_obj = {f"labelName": label_name, "count": value, "snippetCount": 1, "fileCount": file_count}
                data_source_findings[label_name] = dict_obj
                data_source_findings[label_name]["snippets"] = [snippet.dict()]

    def _get_doc_report_metadata(self, doc, report_metadata_init):
        logger.debug("In Function: _get_doc_report_metadata")
        loader_source_snippets = report_metadata_init["loader_source_snippets"]
        total_findings = report_metadata_init["total_findings"]
        snippet_count = report_metadata_init["snippet_count"]
        file_count = report_metadata_init["file_count"]
        data_source_snippets = report_metadata_init["data_source_snippets"]
        data_source_findings = report_metadata_init["data_source_findings"]

        # getting snippet details only if snippet has restricted entities or topics.
        findings = doc["entityCount"] + doc["topicCount"]
        source_path = doc.get("sourcePath")
        if source_path in loader_source_snippets.keys():
            loader_source_snippets[source_path] = loader_source_snippets[source_path] + findings
            total_findings += findings
            snippet_count += 1
        else:
            loader_source_snippets[source_path] = findings
            total_findings += findings
            snippet_count += 1
            file_count += 1

        if len(doc["topics"]) > 0:
            self._get_finding_details(doc, data_source_findings, "topics", file_count)
        if len(doc["entities"]) > 0:
            self._get_finding_details(doc, data_source_findings, "entities", file_count)

        report_metadata_init["loader_source_snippets"] = loader_source_snippets
        report_metadata_init["total_findings"] = total_findings
        report_metadata_init["snippet_count"] = snippet_count
        report_metadata_init["file_count"] = file_count
        report_metadata_init["data_source_snippets"] = data_source_snippets
        report_metadata_init["data_source_findings"] = data_source_findings
        return report_metadata_init

    def _generate_final_report(self, report_metadata_init):
        logger.debug("In Function: _generate_final_report")
        loader_source_snippets = report_metadata_init["loader_source_snippets"]
        file_count_restricted_data = len(loader_source_snippets)
        report_summary = Summary(
            findings=report_metadata_init["total_findings"],
            totalFiles=report_metadata_init["file_count"],
            filesWithRestrictedData=file_count_restricted_data,
            dataSources=report_metadata_init["data_source_count"],
            owner=self.app_details["owner"]
        )

        # Filter 5 Findings
        top_5_findings = sorted(loader_source_snippets.items(), key=lambda d: d[1], reverse=True)[:5]
        top_5_finding_objects = [{"fileName": filename, "count": count} for filename, count in top_5_findings]

        # Generating DataSource
        data_source_obj_list = list()
        logger.debug(report_metadata_init["data_source_findings"])
        for loader in self.app_details["loaders"]:
            name = loader.get("name")
            source_path = loader.get("sourcePath")
            source_type = loader.get("sourceType")
            data_source_findings = [ {key: value[key] for key in value if key != value[key] } for value in report_metadata_init["data_source_findings"].values()]
            data_source_obj = DataSource(name=name, sourcePath=source_path, sourceType=source_type,
                                         summary=report_summary,
                                         findings=data_source_findings,
                                         snippets=report_metadata_init["data_source_snippets"])
            data_source_obj_list.append(data_source_obj)

        report_dict = ReportModel(
            name=self.app_details["name"],
            description="",  # self.app_details["description"],
            instanceDetails=self.app_details["instanceDetails"],
            framework=self.app_details["framework"],
            reportSummary=report_summary,
            topFindings=top_5_finding_objects,
            lastModified=datetime.now(),
            dataSources=data_source_obj_list
        )

        return report_dict.dict()

    def process_docs_and_generate_report(self):
        input_doc_list = self.data.get('docs', [])
        logger.debug("In Function: _get_doc_details_and_generate_report")
        metadata_obj = Metadata(createdAt=datetime.now(), modifiedAt=datetime.now())
        last_used = datetime.now()
        loader_details = self.data.get("loader_details", {})
        docs = self.app_details.get("docs", [])
        report_metadata_init = {"total_findings": 0, "data_source_count": 1, "data_source_snippets": list(),
                                "loader_source_snippets": {}, "file_count": 0, "snippet_count": 0,
                                "data_source_findings": {}}
        loader_source_files = self.app_details.get("loader_source_files", [])
        for doc in input_doc_list:
            # Get classifier Response
            if doc:
                doc_info: AiDataModel = self._get_classifier_response(doc)
                doc_model = AiDocs(appId=self.load_id,
                                   metadata=metadata_obj,
                                   doc=doc.get('doc'),
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
        loader_source_files.append(
            [{"name": f"{key}", "count": loader_source_snippets[key]} for key in loader_source_snippets])
        self.app_details["loader_source_files"] = loader_source_files

        # Generate Final Report
        final_report = self._generate_final_report(report_metadata_init)
        return self.app_details, final_report

