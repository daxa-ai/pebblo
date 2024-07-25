import { SearchIcon } from "../icons/index.js";
import { EmptyState } from "./index.js";
import { KEYWORD_MAPPING } from "../constants/keywordMapping.js";
import { getFormattedDate } from "../util.js";

const KeyValueBlock = (props) => {
  const { label, content, subText } = props;
  return /*html*/ `<div class="surface-10 inter flex flex-col gap-2">
    <div class="flex gap-2">
      <div class="font-12 semi-bold">${label}</div>
      ${
        subText
          ? `<div class="font-12 surface-10-opacity-50">| ${subText}</div>`
          : ""
      }
    </div>
    <div class="font-13">${content || "-"}</div>
  </div>`;
};

const constructFindingsStr = (findings) => {
  if (findings && Object.keys(findings)?.length > 0) {
    return Object.keys(findings)
      .map((item) => KEYWORD_MAPPING[item] || item)
      .join(" | ");
  }
  return "";
};

export function RetrievalDetails(props) {
  const { title, data, searchField, inputPlaceholder, error } = props;
  return /*html*/ ` <div class="tab_panel snippet-details-container flex flex-col gap-4">
    <div class="flex justify-between inter items-center">
    <div>
    <div class="flex items-center gap-2">
      <div class="surface-10 font-16 medium">Retrievals</div>
      <div class="font-12 surface-10-opacity-50">Showing ${
        data?.length || 0
      } out of ${data?.length || 0}</div>
    </div>
    <div class="font-12"></div>
    </div>
    <div class="flex">
      
    </div>
  </div>
  ${
    !error
      ? `<div id="snippet_body" class="flex flex-col gap-4 h-full">
  ${
    data?.length
      ? data?.myMap((item) => {
          const promptInfo = `By ${item?.user || "-"}, ${
            getFormattedDate(item?.prompt_time, true, true) || ""
          }`;
          const contextInfo =
            item?.context && item?.context[0]
              ? `From ${item?.context[0]?.vector_db || ""}`
              : "";
          const retrievedFrom =
            item?.context && item?.context[0]
              ? item?.context[0]?.retrieved_from || "-"
              : "-";
          const findings = constructFindingsStr(item?.prompt?.entities);
          return /*html*/ `
          <div class="flex flex-col gap-1">
             <div class="snippet-body flex flex-col gap-4 pr-3 pl-3 pt-3 pb-3">
                <div>
                 ${KeyValueBlock({
                   label: "Prompt",
                   content: item?.prompt?.data,
                   subText: promptInfo,
                 })}
                 ${
                   findings
                     ? `<div class="mt-2 w-fit flex gap-2 items-center pb-2 pr-2 w-auto inter">
                       <div class="surface-10-opacity-50 semi-bold font-12">
                         Findings:
                       </div>
                       <div class="font-13">${findings}</div>
                     </div>`
                     : ""
                 }
                </div>
                 ${KeyValueBlock({
                   label: "Context",
                   content: item?.context[0]?.doc,
                   subText: contextInfo,
                 })}
                 ${KeyValueBlock({
                   label: "Response",
                   content: item?.response?.data,
                   subText: "",
                 })}
                 <div class="w-fit flex gap-2 border-grey-20 items-center pt-3 pb-3 pl-2 pr-2 w-auto inter">
                 <div class="font-12 semi-bold">Retrieved from: </div>
                 <div class="font-13">${retrievedFrom}</div>
                 </div>
       
               <div class="divider-horizontal"></div>
             </div>
           </div>
               `;
        })
      : /*html*/ `<div class="text-center pt-3 pb-3 pl-3 pr-3 inter surface-10 font-13 medium">No Data Found!!</div>`
  }
    </div>`
      : EmptyState({ variant: error })
  }
    </div>`;
}
