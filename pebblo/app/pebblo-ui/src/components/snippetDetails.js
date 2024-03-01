import { MEDIA_URL } from "../constants/constant.js";
import { KEYUP } from "../constants/enums.js";
import { waitForElement } from "../util.js";
import { KeyValue } from "./index.js";

export function SnippetDetails(props) {
  const { title, data, searchField } = props;

  waitForElement("#snippet_search", 1000).then(function () {
    const inputEl = document.getElementById("snippet_search");
    if (inputEl) inputEl?.addEventListener(KEYUP, onChange);
  });

  function onChange(evt) {
    let filteredData;
    if (evt.target.value) {
      filteredData = data?.filter((item) =>
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
      filteredData = data;
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
      <div class="snippet-details-container flex flex-col gap-4">
      <div class="flex justify-between">
        <div class="inter surface-10 font-16 medium">${title}</div>
        <div class="flex">
          <div class="search">
            <input type="text" id="snippet_search" autocomplete="off" />
            <img
              src="${MEDIA_URL}/static/search-icon.png"
              alt="Search Icon" />
          </div>
        </div>
      </div>
      <div id="snippet_body" class="flex flex-col gap-10 h-full">
         ${
           data?.length
             ? data?.myMap(
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
                   <div class="divider-horizontal"></div>
                  </div>
                `
              )}
          </div>
        `
               )
             : /*html*/ `<div class="text-center pt-3 pb-3 pl-3 pr-3 inter surface-10 font-13 medium">No Data Found!!</div>`
         }
      </div>
  </div>
    `;
}
