import { SearchIcon } from "../icons/index.js";
import { EmptyState } from "./index.js";
import { KEYWORD_MAPPING } from "../constants/keywordMapping.js";

const KeyValueBlock = (props) => {
  const { label, content } = props;
  return /*html*/ `<div class="surface-10 inter flex flex-col gap-2">
    <div>
      <div class="font-12 semi-bold">${label}</div>
    </div>
    <div class="font-13">${content}</div>
  </div>`;
};

export function RetrievalDetails(props) {
  const { title, data, searchField, inputPlaceholder, error } = props;
  return /*html*/ ` <div class="tab_panel snippet-details-container flex flex-col gap-4">
    <div class="inter flex gap-2 items-center">
    <div class="surface-10 font-16 medium">${title}</div>
    </div>
    <div class="flex justify-between inter items-center">
    <div>
    <div class="flex items-center gap-2">
      <div class="surface-10 font-16 medium">Retrieval</div>
    </div>
    <div class="font-12"></div>
    </div>
    <div class="flex">
      <div class="search">
        <input type="text" id="snippet_search" placeholder="${inputPlaceholder}" autocomplete="off" />
          ${SearchIcon({ color: "grey" })}  
      </div>
    </div>
  </div>
  ${
    !error
      ? `<div id="snippet_body" class="flex flex-col gap-10 h-full">
  ${
    data?.snippets?.length
      ? data?.snippets?.myMap(
          (item) => /*html*/ `        
     <div class="flex flex-col gap-1">
       <div class="snippet-header bg-main flex gap-2 pt-3 pb-3 pl-3 pr-3 inter items-center">
         <div class="surface-10-opacity-65 font-14 medium">${
           KEYWORD_MAPPING[item?.labelName] || item?.labelName
         }</div>
         <div class="surface-10-opacity-50 font-12">Showing ${
           item?.snippets?.length
         } out of ${item?.snippetCount}</div>
       </div>
       ${item?.snippets?.myMap(
         (snipp) => `
            <div class="snippet-body flex flex-col gap-3 pr-3 pl-3 pt-3 pb-3">
             ${KeyValueBlock({ label: "Prompt", content: snipp?.snippet })}
             ${KeyValueBlock({ label: "Context", content: snipp?.snippet })}
            <div class="divider-horizontal"></div>
           </div>
         `
       )}
    </div>
        `
        )
      : /*html*/ `<div class="text-center pt-3 pb-3 pl-3 pr-3 inter surface-10 font-13 medium">No Data Found!!</div>`
  }
    </div>`
      : EmptyState({ variant: error })
  }
    </div>`;
}
