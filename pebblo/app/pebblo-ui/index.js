const MEDIA_URL = document.currentScript.getAttribute("staticURL");
const APP_DATA = JSON.parse(document.currentScript.getAttribute("appData"));
let tabValue = 0;
const TABLE_DATA_FOR_APPLICATIONS = [
  {
    label: "Application",
    field: "application",
    application: APP_DATA?.name,
    align: "start",
  },
  {
    label: "Findings - Topics",
    field: "topics",
    topics: APP_DATA?.reportSummary.findingsTopics,
    align: "end",
  },
  {
    label: "Findings - Entities",
    field: "entities",
    entities: APP_DATA?.reportSummary.findingsEntities,
    align: "end",
  },
  {
    label: "Owner",
    field: "owner",
    owner: APP_DATA?.reportSummary.owner,
    align: "start",
  },
  {
    label: "",
    field: "actions",
    actions: `
      <div class="flex gap-4 justify-end">
      <img class="cursor-pointer" src="${MEDIA_URL}/static/download-icon.png" alt="Download Icon" />
      <div class="divider"></div>
      <img class="cursor-pointer" src="${MEDIA_URL}/static/pending-icon.png" alt="Download Icon" />
      </div>
    `,
  },
];

const TABLE_DATA_FOR_FINDINGS = [
  {
    label: "Finding type",
    field: "type",
    type: APP_DATA?.name,
    align: "start",
  },
  {
    label: "Finding",
    field: "finding",
    finding: APP_DATA?.reportSummary.findingsTopics,
    align: "start",
  },
  {
    label: "Source Files",
    field: "sourceFiles",
    sourceFiles: APP_DATA?.reportSummary.findingsEntities,
    align: "end",
  },
  {
    label: "Snippets",
    field: "snippets",
    snippets: APP_DATA?.reportSummary.owner,
    align: "start",
  },
  {
    label: "Data Source",
    field: "dataSource",
    dataSource: APP_DATA?.reportSummary.owner,
    align: "start",
  },
  {
    label: "Application",
    field: "application",
    application: "",
    align: "start",
  },
];

const TABLE_DATA_FOR_FILES_WITH_FINDINGS = [
  {
    label: "File Name",
    field: "fileName",
    fileName: "",
    align: "start",
  },
  {
    label: "Findings-Topics",
    field: "findingsTopics",
    findingsTopics: "",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "findingsEntities",
    findingsEntities: "",
    align: "end",
  },
  {
    label: "Data Source",
    field: "datasource",
    datasource: "",
    align: "start",
  },
  {
    label: "Application",
    field: "application",
    application: "",
    align: "start",
  },
];

const TABLE_DATA_FOR_DATA_SOURCE = [
  {
    label: "Data Source Name",
    field: "dataSourceName",
    render: (item) => `
    <div class="flex flex-col inter">
       <div class="surface-10 font-13">${item.dataSourceName || "-"}</div>
       <div class="surface-10-opacity-50 font-12">-</div>
    </div>
 `,
    align: "start",
  },
  {
    label: "Findings-Topics",
    field: "findingsTopics",
    findingsTopics: "",
    align: "end",
  },
  {
    label: "Findings-Entities",
    field: "findingsEntities",
    findingsEntities: "",
    align: "end",
  },
  {
    label: "Application",
    field: "application",
    application: "",
    align: "start",
  },
];

const APP_DETAILS_FINDINGS_TABLE = [
  {
    label: "Finding type",
    field: "type",
    type: APP_DATA?.name,
    align: "start",
  },
  {
    label: "Finding",
    field: "finding",
    finding: APP_DATA?.reportSummary.findingsTopics,
    align: "end",
  },
  {
    label: "Source Files",
    field: "sourceFiles",
    sourceFiles: APP_DATA?.reportSummary.findingsEntities,
    align: "end",
  },
  {
    label: "Snippets",
    field: "snippets",
    snippets: APP_DATA?.reportSummary.owner,
    align: "start",
  },
  {
    label: "Data Source",
    field: "dataSource",
    dataSource: APP_DATA?.reportSummary.owner,
    align: "start",
  },
];

const TABS_ARR_FOR_APPLICATIONS = [
  {
    label: "Applications With Findings",
    critical: 2,
    outOf: 4,
    value: 0,
    isCritical: true,
    tabPanel: ApplicationsList("Applications", TABLE_DATA_FOR_APPLICATIONS),
  },
  {
    label: "Findings",
    critical: 72,
    outOf: 0,
    value: 1,
    isCritical: true,
    tabPanel: ApplicationsList("Findings", TABLE_DATA_FOR_FINDINGS),
  },
  {
    label: "Files With Findings",
    critical: 8,
    outOf: 24,
    value: 2,
    isCritical: true,
    tabPanel: ApplicationsList(
      "Files With Findings",
      TABLE_DATA_FOR_FILES_WITH_FINDINGS
    ),
  },
  {
    label: "Data Source",
    critical: 4,
    outOf: 0,
    value: 3,
    isCritical: false,
    tabPanel: ApplicationsList("Data Source", TABLE_DATA_FOR_DATA_SOURCE),
  },
];

const TABS_ARR_FOR_APPLICATION_DETAILS = [
  {
    label: "Findings",
    critical: 72,
    outOf: 0,
    value: 0,
    isCritical: true,
    tabPanel: Application_Details_List_Section(
      "Findings",
      APP_DETAILS_FINDINGS_TABLE
    ),
  },
  {
    label: "Files With Findings",
    critical: 8,
    outOf: 24,
    value: 1,
    isCritical: true,
    tabPanel: Application_Details_List_Section(
      "Files With Findngs",
      APP_DETAILS_FINDINGS_TABLE
    ),
  },
  {
    label: "Data Source",
    critical: 4,
    outOf: 0,
    value: 2,
    isCritical: false,
    tabPanel: Application_Details_List_Section(
      "Data Source",
      APP_DETAILS_FINDINGS_TABLE
    ),
  },
  {
    label: "Snippets",
    critical: 254,
    outOf: 0,
    value: 3,
    isCritical: false,
    tabPanel: SnippetDetails(APP_DATA?.dataSources[0]?.findingsDetails),
  },
];

const APP_DETAILS = [
  {
    label: "IP",
    value: "49.248.66.146",
  },
  {
    label: "Runtime",
    value: "Local",
  },
  {
    label: "Language",
    value: "Python 3.10.12",
  },
  {
    label: "Host",
    value: "OPLPT012.local",
  },
  {
    label: "Created At",
    value: "2024-01-18 10:57:29",
  },
  {
    label: "Path",
    value:
      "/Users/shreyasdamle/work/cloud_defense/daxa-analyzer-rc1/samples/basic_retrieval",
  },
];

document.getElementById("root").innerHTML = `${App()}`;

// <APP_COMPONENT>

function App() {
  let UI;
  let isDetailPage = window.location.pathname === "/";
  if (isDetailPage) {
    UI = Overview;
  } else {
    UI = AppDetailsPage;
  }
  return `
     <div class="app">
        ${Header()}
        <div class="h-full flex flex-col pt-9 pb-9 pl-25 pr-25 gap-3 overflow-hidden">
        ${
          !isDetailPage
            ? Button({
                variant: "text",
                btnText: "Back",
                startIcon: "/static/back-icon.png",
                href: "/",
              })
            : ""
        }
           ${Card(UI())}
        </div>
     </div>
    `;
}

// </APP_COMPONENT>

// <HEADER_COMPONENT> ----------->

function Header() {
  return ` <div id="header" class="relative pt-4 pb-4 pl-6 pr-6 bg-white">
              <img class="cursor-pointer" src="${MEDIA_URL}/static/pebblo-icon.png" alt="Pebblo Icon" />
              <div class="mask absolute top-0 bg-grey-70 h-59 w-full left-0 -z-1"></div>
           </div>`;
}

// </HEADER_COMPONENT>

// <CARD_COMPONENT> ----------->

function Card(children) {
  return `
    <div class="card overflow-hidden">${children}</div>
    `;
}

// </CARD_COMPONENT>

// <OVERVIEW_COMPONENT> ----------->

function Overview() {
  return `
     <div class="flex gap-5 flex-col h-full overflow-auto">
      <div class="surface-10 inter font-14 medium">Overview</div>
       ${Tabs(
         TABS_ARR_FOR_APPLICATIONS,
         ApplicationsList("Applications", TABLE_DATA_FOR_APPLICATIONS)
       )}
     </div>
    `;
}

// </OVERVIEW_COMPONENT>

// <TABS_COMPONENT> ----------->

function Tabs(tabsArr, children) {
  let allTabs = "";
  tabsArr?.map((tab) => (allTabs += Tab(tab)));
  document.addEventListener("DOMContentLoaded", function () {
    const tabElements = document.getElementsByClassName("tab");
    Array.from(tabElements).forEach((element) => {
      element?.addEventListener("click", function (e) {
        tabValue = Number(e.target.dataset.value);
        document.getElementById("tab-selected").style.left = `${
          Number(e.target.dataset.value) * 224 +
          (Number(e.target.dataset.value)
            ? 24 * Number(e.target.dataset.value)
            : 0)
        }px`;
        const tabPanel = document.getElementById("tab-panel");
        tabPanel.innerHTML = "";
        tabPanel.innerHTML = tabsArr[tabValue]?.tabPanel;
      });
    });
  });

  return `
    <div class="flex flex-col">
      <div class="tabs sticky top-0 flex gap-6">
        ${allTabs}
        <div id="tab-selected"></div> 
      </div>
      <div id="tab-panel" class="h-full">${children}</div>
    </div>
    `;
}

// </TABS_COMPONENT>

// <TAB_COMPONENT> ----------->

function Tab(item) {
  return `
        <div class="tab manrope" data-value=${item?.value}>
          <div class="inline ${
            item?.isCritical ? "critical" : "surface-10"
          } font-48 font-thin pointer-none">
           ${item?.critical < 10 ? `0${item?.critical}` : item?.critical} ${
    item?.outOf
      ? `<span class="surface-10 font-24 -ml-1">/${item?.outOf}</span>`
      : ""
  }
          </div>
          <div class="font-13 inter surface-10 pointer-none">${
            item?.label
          }</div>
        </div>
       
    `;
}

// </TAB_COMPONENT>

// <TABLE_COMPONENT> ----------->

function Table(tableData, link) {
  return `<table cellspacing="0" cellpadding="0">
  ${Thead(tableData)}
  ${Tbody(tableData, link)}
  </table>`;
}

function Thead(tableData) {
  return `
    <thead>${tableData
      ?.map((item) => {
        const className =
          item?.align === "start"
            ? "text-start"
            : item?.align === "center"
            ? "text-center"
            : "text-end";
        return `<th class="${className}">${item.label}</th>`;
      })
      .join("")}</thead>
  `;
}

function Tbody(tableData, link) {
  return `
    <tbody>
     <tr class="table-row">
     ${tableData
       ?.map((item) =>
         Td(
           item?.render ? item?.render(item) : item[item?.field],
           item?.align,
           item?.field !== "actions" && link
             ? `${link}/?id=${tableData?.id}`
             : ""
         )
       )
       .join("")}
     </tr>
    </tbody>
  `;
}

function Td(children, align, link) {
  const className =
    align === "start"
      ? "text-start"
      : align === "center"
      ? "text-center"
      : "text-end";

  if (link) {
    return `
    <td class="${className} pt-3 pb-3 pl-3 pr-3">
    ${children || "-"}
        <a href="${link}" id="link"><a/>
    </td>
 `;
  }
  return `
     <td class="${className} pt-3 pb-3 pl-3 pr-3">
     ${children || "-"}
     </td>
  `;
}

// </TABLE_COMPONENT>

// </BUTTON_COMPONENT> ----------->

function Button({ variant = "text", btnText, startIcon, endIcon, href }) {
  if (href) {
    return `
  <a href="${href}" class="link w-fit">
    <button class="relative ${variant}">
        <div class="flex gap-1 items-center">
        ${
          startIcon
            ? `<img src="${MEDIA_URL}${startIcon}" alt="Start Icon" />`
            : ``
        }
        <span>${btnText}</span>
        ${endIcon ? `<img src="${MEDIA_URL}${endIcon}" alt="End Icon" />` : ``}
        </div>
      </button>
  </a>  
      `;
  }

  return `<button class="relative ${variant}">
      <div class="flex gap-1 items-center">
      ${
        startIcon
          ? `<img src="${MEDIA_URL}${startIcon}" alt="Start Icon" />`
          : ``
      }
       <span>${btnText}</span>
       ${endIcon ? `<img src="${MEDIA_URL}${endIcon}" alt="End Icon" />` : ``}
     </div>
      </button>`;
}

// </BUTTON_COMPONENT>

{
  /* <ACCORDION_COMPONENT> */
}

function AccordionSummary(children, id) {
  document.addEventListener("DOMContentLoaded", function () {
    const accordion = document.getElementsByClassName("accordion-summary");
    Array.from(accordion)?.forEach((acc) => {
      acc.addEventListener("click", function (e) {
        this.classList.toggle("active");
        let panel = document.getElementById(
          `panel-${Number(e.target.parentElement.dataset.value)}`
        );
        if (panel.style.display === "flex") {
          panel.style.display = "none";
        } else {
          panel.style.display = "flex";
        }
      });
    });
  });
  return ` 
     <button title="Accordion-summary" type="button" class="accordion-summary flex gap-1 items-center" data-value="${id}">
      <div>${children}</div>
      <img id="arrow-icon" src="${MEDIA_URL}/static/arrow.png" alt="Arrow icon"/>
     </button>
  `;
}

function AccordionDetails(children, id) {
  return `
     <div title="Accordion-details" id="${id}" class="accordion-details">
         ${children}
     </div>
  `;
}

// </ACCORDION_COMPONENT>

// <APPLICATION_LIST_COMPONENT> ----------->

function ApplicationsList(title, tableData) {
  const navigateToDetailsPage = "/appDetails";
  return `
  <div class="application-container flex flex-col gap-4">
  <div class="flex justify-between">
    <div class="inter surface-10 font-16 medium">${title}</div>
    <div class="flex">
      <div class="search">
        <input type="text" />
        <img
          src="${MEDIA_URL}/static/search-icon.png"
          alt="Search Icon" />
      </div>
      <div class="divider mt-2 mb-2 ml-4 mr-1"></div>
      ${Button({
        btnText: "Download Reports",
        startIcon: "/static/download-icon.png",
      })}
    </div>
  </div>
  ${Table(tableData, navigateToDetailsPage)}
</div>
  `;
}
// </APPLICATION_LIST_COMPONENT>

// APP DETAILS PAGE ----------->

function AppDetailsPage() {
  return `
  <div class="flex gap-6 flex-col h-full overflow-auto">
    <div class="flex justify-between">
      <div class="flex gap-3">
         <div class="bg-surface-10 pl-2 pr-2 pt-4 pb-4 rounded-lg">
           <img src="${MEDIA_URL}/static/langchain-icon.png" alt="App icon" />
         </div>
         <div class="flex flex-col gap-1 inter surface-10">
           <div class="font-24">${APP_DATA?.name}</div>
           <div class="font-12 flex gap-3">
             <div class="font-thin">Last Updated 10 Jan 2024</div>
             <div class="divider"></div>
             ${AccordionSummary("Instance Details", 1)}
           </div>
         </div>
      </div>
      <div class="flex gap-2 mt-auto h-fit">
        ${Button({
          variant: "text",
          btnText: "Download Report",
          startIcon: "/static/download-icon.png",
        })}
        <div class="divider mt-2 mb-2"></div>
        ${Button({
          variant: "text",
          btnText: "Load History",
          startIcon: "/static/pending-icon.png",
        })}
      </div>
    </div>
    ${AccordionDetails(
      `<div class="grid grid-cols-4 row-gap-3">
         ${APP_DETAILS?.map((item) => KeyValue(item.label, item.value)).join(
           ""
         )}
      </div>`,
      "panel-1"
    )}
    <div class="divider-horizontal"></div>
    <div class="flex flex-col gap-4 h-full">
      <div class="flex gap-2 surface-10 inter items-center">
         <div class="font-16">Report Summary</div>
         <div class="font-12">Current Load By ${
           APP_DATA?.reportSummary?.owner
         }, 10 Jan 2024 </div>
      </div>
      ${Tabs(
        TABS_ARR_FOR_APPLICATION_DETAILS,
        Application_Details_List_Section("Findings", APP_DETAILS_FINDINGS_TABLE)
      )}
    </div>
 </div>
  `;
}

function Application_Details_List_Section(title, tableData) {
  return `
  <div class="application-container flex flex-col gap-4">
    <div class="flex justify-between">
      <div class="inter surface-10 font-16 medium">${title}</div>
        <div class="search">
          <input type="text" />
          <img
            src="${MEDIA_URL}/static/search-icon.png"
            alt="Search Icon" />
        </div>
    </div>
    ${Table(tableData)}
  </div>
  `;
}

function SnippetDetails(snippetDetails) {
  return `
    <div class="flex flex-col gap-10 h-full">
       ${snippetDetails
         ?.map(
           (item) => ` 
          
          <div class="flex flex-col gap-1">
            <div class="snippet-header bg-main flex gap-2 pt-3 pb-3 pl-3 pr-3 inter">
              <div class="surface-10-opacity-65 font-14 medium">${
                item?.labelName
              }</div>
              <div class="surface-10-opacity-50 font-12">Showing ${
                item?.snippetCount
              } out of ${item?.findings}</div>
            </div>
            ${item?.snippets
              ?.map(
                (snipp) => `
                 <div class="snippet-body flex flex-col gap-3 pr-3 pl-3 pt-3 pb-3">
                  ${KeyValue("Snippets", snipp?.snippet)}
                  ${KeyValue("Retrieved From", snipp?.sourcePath)}
                 <div class="divider-horizontal"></div>
                </div>
              `
              )
              .join("")}
        </div>
      `
         )
         .join("")}
    </div>
  `;
}

function KeyValue(key, value) {
  return `
    <div class="flex flex-col gap-2 inter">
       <div class="surface-60 font-12">${key}</div>
       <div class="surface-10 font-13">${value}</div>
    </div>
  `;
}
