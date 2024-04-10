import { KEYUP } from "../constants/enums.js";
import { SearchIcon } from "../icons/index.js";
import { waitForElement } from "../util.js";
import { EmptyState } from "./emptyState.js";
import { KeyValue } from "./index.js";

// PROPS {
//   title: string,
//   data: Array<unknown>,
//   searchField: Array<string>
// }

export function SnippetDetails(props) {
  const { title, data, searchField, inputPlaceholder, error } = props;

  waitForElement("#snippet_search", 1000).then(function () {
    const inputEl = document.getElementById("snippet_search");
    if (inputEl) inputEl?.addEventListener(KEYUP, onChange);
  });

  function onChange(evt) {
    let filteredData;
    if (evt.target.value) {
      filteredData = data?.snippets?.filter((item) =>
        eval(
          searchField
            ?.map((sch) =>
              item[sch]
                ?.toLocaleLowerCase()
                ?.includes(evt.target.value.toLocaleLowerCase())
            )
            .join(" || ")
        )
      );
    } else {
      filteredData = data?.snippets;
    }
    const snippet_body = document.getElementById("snippet_body");
    snippet_body.innerHTML = "";
    snippet_body.innerHTML = filteredData?.length
      ? filteredData?.myMap(
          (item) => /*html*/ `        
       <div class="flex flex-col gap-1">
         <div class="snippet-header bg-main flex gap-2 pt-3 pb-3 pl-3 pr-3 inter items-center">
           <div class="surface-10-opacity-65 font-14 medium">${
             item?.labelName
           }</div>
           <div class="surface-10-opacity-50 font-12">Showing ${
             item?.snippetCount
           } out of ${item?.findings}</div>
         </div>
         ${item?.snippets?.myMap(
           (snipp) => `
              <div class="snippet-body flex flex-col gap-3 pr-3 pl-3 pt-3 pb-3">
               ${KeyValue({ key: "Snippets", value: snipp?.snippet })}
               ${KeyValue({
                 key: "Retrieved From",
                 value: snipp?.sourcePath,
               })}
               ${KeyValue({
                 key: "Identity",
                 value:
                   snipp?.authorizedIdentities?.length > 0
                     ? snipp?.authorizedIdentities.join(", ")
                     : "-",
               })}
              <div class="divider-horizontal"></div>
             </div>
           `
         )}
     </div>
   `
        )
      : /*html*/ `<div class="text-center pt-3 pb-3 pl-3 pr-3 inter surface-10 font-13 medium">No Data Found!!</div>`;
  }

  return /*html*/ `
      <div class="tab_panel snippet-details-container flex flex-col gap-4">
      <div class="flex justify-between">
        <div class="inter flex gap-2 items-center">
        <div class="surface-10 font-16 medium">${title}</div>
        <div class="surface-10-opacity-50 font-12">Showing ${
          data?.snippetCount
        } out of ${data?.totalSnippetCount}</div>
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
               item?.labelName
             }</div>
             <div class="surface-10-opacity-50 font-12">Showing ${
               item?.snippets?.length
             } out of ${item?.snippetCount}</div>
           </div>
           ${item?.snippets?.myMap(
             (snipp) => `
                <div class="snippet-body flex flex-col gap-3 pr-3 pl-3 pt-3 pb-3">
                 ${KeyValue({ key: "Snippets", value: snipp?.snippet })}
                 ${KeyValue({
                   key: "Retrieved From",
                   value: snipp?.sourcePath,
                 })}
                ${KeyValue({
                  key: "Identity",
                  value:
                    snipp?.authorizedIdentities?.length > 0
                      ? snipp?.authorizedIdentities.join(", ")
                      : "-",
                })}
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
  </div>
    `;
}
