import { KEYUP } from "../constants/enums.js";
import { KEYWORD_MAPPING } from "../constants/keywordMapping.js";
import { SearchIcon } from "../icons/index.js";
import { waitForElement } from "../util.js";
import { EmptyState } from "./emptyState.js";
import { KeyValue } from "./index.js";
import { Tooltip } from "./tooltip.js";

function DisplaySnippet(props) {
  const { formattedString } = props;
  return `<div>
      ${formattedString.myMap((item, index) =>
        item?.score
          ? Tooltip({
              children: `<span class="confidence-score">${item.string}</span>`,
              title: `Confidence: ${item?.score}`,
              variant: "top",
              inline: true,
              width: "width-max-content",
            })
          : `<span >${item.string}</span>`
      )}
    </div>`;
}

export function SnippetDetails(props) {
  const { title, data, searchField, inputPlaceholder, error } = props;

  waitForElement("#snippet_search", 1000).then(function () {
    const inputEl = document.getElementById("snippet_search");
    if (inputEl) inputEl?.addEventListener(KEYUP, onChange);
  });

  let snippetList = [];

  const splitStringByPivots = (longString, pivots, groups, scores) => {
    return pivots
      .reduce((result, end, index) => {
        const start = index === 0 ? 0 : pivots[index - 1];
        result.push({
          string: longString.slice(start, end),
          isEntity: groups.includes(`${start}_${end}`),
          score: scores[groups.indexOf(`${start}_${end}`)] || "",
        });
        return result;
      }, [])
      .concat({
        string: longString.slice(pivots[pivots.length - 1]),
      });
  };

  const extractLocations = (entityDetails) => {
    return Object.values(entityDetails || {})
      .flatMap((entries) =>
        entries.map((entry) => entry.location.split("_").map(Number))
      )
      .flat();
  };

  const extractLocationStrings = (entityDetails) => {
    return Object.values(entityDetails || {}).flatMap((entries) =>
      entries.map((entry) => entry.location)
    );
  };

  const extractConfidenceScore = (entityDetails) => {
    return Object.values(entityDetails || {}).flatMap((entries) =>
      entries.map((entry) => entry.confidence_score)
    );
  };

  if (data?.snippets?.length > 0) {
    snippetList = data?.snippets?.map((snippetObj) => {
      let snippetStrings = {};
      snippetStrings = snippetObj?.snippets?.map((snippetDetails) => {
        const { snippet, entityDetails } = snippetDetails;
        const locations = extractLocations(entityDetails);
        const locationStrings = extractLocationStrings(entityDetails);
        const confidenceScores = extractConfidenceScore(entityDetails);
        let string = "";
        if (locations && locationStrings && snippet)
          string = splitStringByPivots(
            snippet,
            locations,
            locationStrings,
            confidenceScores
          );
        if (string) return { string, ...snippetDetails };
        else return snippetDetails;
      });
      return { ...snippetObj, snippetStrings };
    });
  }

  const getSnippetConfidenceScore = (item, snipp) => {
    const topic = item?.labelName;
    if (item && topic && snipp?.topicDetails && snipp?.topicDetails[topic]) {
      const topicDetails = snipp?.topicDetails[topic];
      if (topicDetails?.length > 0) {
        return `Confidence: ${topicDetails[0]?.confidence_score}`;
      }
    }
    return "";
  };

  function onChange(evt) {
    let filteredData;
    if (evt.target.value) {
      filteredData = snippetList?.filter((item) =>
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
      filteredData = snippetList;
    }
    const snippet_body = document.getElementById("snippet_body");
    snippet_body.innerHTML = "";
    snippet_body.innerHTML = filteredData?.length
      ? filteredData?.myMap(
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
         ${item?.snippetStrings?.myMap((snipp) => {
           const snippetConfidenceScore = getSnippetConfidenceScore(
             item,
             snipp
           );
           return `
              <div class="snippet-body flex flex-col gap-3 pr-3 pl-3 pt-3 pb-3">
               ${KeyValue({
                 key: `Snippets ${
                   snippetConfidenceScore ? `| ${snippetConfidenceScore}` : ""
                 }`,
                 value: DisplaySnippet({
                   formattedString: snipp?.string || [],
                 }),
               })}
               ${KeyValue({
                 key: "Retrieved from",
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
           `;
         })}
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
        snippetList
          ? snippetList?.myMap(
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
           ${item?.snippetStrings?.myMap((snipp) => {
             const snippetConfidenceScore = getSnippetConfidenceScore(
               item,
               snipp
             );
             return `
                <div class="snippet-body flex flex-col gap-3 pr-3 pl-3 pt-3 pb-3">
                 ${KeyValue({
                   key: `Snippets ${
                     snippetConfidenceScore ? `| ${snippetConfidenceScore}` : ""
                   }`,
                   value: DisplaySnippet({
                     formattedString: snipp?.string || [],
                   }),
                 })}
                 ${KeyValue({
                   key: "Retrieved from",
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
             `;
           })}
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
