import { KEYUP, LOAD, ACTIONS, CLICK } from "../constants/enums.js";
import { GET_REPORT } from "../constants/routesConstant.js";
import { DownloadIcon, SearchIcon } from "../icons/index.js";
import { GET_FILE } from "../services/get.js";
import { waitForElement } from "../util.js";
import { EmptyState } from "./emptyState.js";
import { Button, Table, Td } from "./index.js";

// PROPS { title: string,
//   tableCol: Array<{
//   label:string;
//   field:string;
//   align?:string;
//   render?:(e)=>void
//   }>,
//   tableData: Array<unknown>,
//   isDownloadReport?: boolean,
//   searchField: Array < string >,
//   isSorting?: boolean,
//   link?: string,
//   inputPlaceholder?: string }

export function ApplicationsList(props) {
  const {
    title,
    tableCol,
    tableData,
    isDownloadReport,
    searchField,
    isSorting,
    link,
    inputPlaceholder = "Search",
    error,
  } = props;

  window.addEventListener(LOAD, function () {
    if (tableCol?.find((col) => col?.field === ACTIONS)) {
      const download_icons = document.getElementsByClassName("download-icon");
      Array.from(download_icons).forEach((icon) => {
        icon?.addEventListener(CLICK, function () {
          GET_FILE(`${GET_REPORT}?app_name=${icon?.id}`);
        });
      });
    }
  });

  waitForElement("#search_field", 1000).then(function () {
    const inputEl = document.getElementById("search_field");
    if (inputEl) inputEl?.addEventListener(KEYUP, onChange);
  });

  function onChange(evt) {
    let filteredData;
    if (evt.target.value) {
      filteredData = tableData?.filter((item) =>
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
      filteredData = tableData;
    }
    document.getElementsByTagName("tbody")[0].innerHTML = filteredData?.length
      ? `
        ${filteredData?.myMap(
          (item, index) => /*html*/ `
            <tr class="table-row">
              ${tableCol?.myMap((col, itemIndex) =>
                Td({
                  children: col?.actions
                    ? col?.actions(item)
                    : col?.render
                    ? col?.render(item)
                    : item[col?.field],
                  align: col?.align,
                  id: `${index}-${itemIndex}`,
                  link:
                    col?.field !== ACTIONS && link
                      ? `${link}?app_name=${item?.name}`
                      : "",
                  maxWidth: col?.type === "label" ? "text-ellipsis" : "fit",
                })
              )}
            </tr>`
        )}
      `
      : /*html*/ ` <tr class="table-row">
             <td class="pt-3 pb-3 pl-3 pr-3 text-center" colspan="${tableCol?.length}">No Data Found</td>
          </tr>`;
  }

  return /*html*/ `
    <div class="tab_panel">
      <div class="application-container flex flex-col gap-4">
        <div class="flex justify-between">
          <div class="inter surface-10 font-16 medium">${title}</div>
          <div class="flex">
            <div class="search" title="Search">
              <input type="text" id="search_field" name="search" placeholder="${inputPlaceholder}" autocomplete="off" />
              ${SearchIcon({ color: "grey" })}  
            </div>
          ${
            isDownloadReport
              ? /*html*/ `<div class="divider mt-2 mb-2 ml-4 mr-1"></div>
              ${Button({
                btnText: "Download Reports",
                startIcon: DownloadIcon({ color: "primary" }),
                color: "primary",
              })}`
              : ""
          }
            </div>
          </div>
          ${
            !error
              ? Table({
                  tableCol,
                  tableData,
                  link,
                  isSorting,
                })
              : EmptyState({ variant: error })
          }
        </div>
    </div>
    `;
}
