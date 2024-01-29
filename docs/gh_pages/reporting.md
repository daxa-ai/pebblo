# Pebblo Data Reports

Pebblo Data Reports provides an in-depth visibilty into the document ingested into Gen-AI RAG application during every load.

This document describes the information produced in the Data Report.

# Report Summary

Report Summary provides the following details:

1. **Findings**: Total number of Topics and Entities found across all the snippets loaded in this specific load run.
1. **Files with Findings**: The number of files that has one or more `Findings` over the total number of files used in this document load. This field indicates the number of files that need to be inspected to remediate any potentially text that needs to be removed and/or cleaned for Gen-AI inference.
1. **Number of Data Source**: The number of data sources used to load documents into the Gen-AI RAG application. For e.g. this field will be two if a RAG application loads data from two different directories or two different AWS S3 buckets.

# Top Files with Most Findings

This table indicates the top files that had the most findings. Typically these files are the most _affending_ ones that needs immediate attention and best ROI for data cleansing and remediation.

# Load History

This table provides the history of findings and path to the reports for the previous loads of the same RAG application.

# Instance Details

This section provide a quick glance of where the RAG application is physically running like in a Laptop (Mac OSX) or Linux VM and related properties like IP address, local filesystem path and Python version.

# Data Source Findings Table

This table provides a summary of all the different Topics and Entities found across all the files that got ingested usind `Pebblo SafeLoader` enabled Document Loaders.

# Snippets

This sections provides the actual text inspected by the `Pebblo Daemon` using the `Pebblo Topic Classifier` and `Pebblo Entity Classifier`. This will be useful to quickly inspect and remediate text that should not be ingested into the Gen-AI RAG application. Each snippet shows the exact file the snippet is loaded from easy remediation.