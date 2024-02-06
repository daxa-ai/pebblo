import { KeyValue } from "./index.js";

export function SnippetDetails(snippetDetails) {
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
