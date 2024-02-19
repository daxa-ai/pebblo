import {
  APP_DETAILS_ROUTE,
  MEDIA_URL,
  APP_DATA,
} from "../constants/constant.js";
import { CHANGE, LOAD, ACTIONS, CLICK } from "../constants/enums.js";
import { GET_FILE } from "../services/get.js";
import { waitForElement } from "../util.js";
import { Button, Table, Td } from "./index.js";

export function ApplicationsList(props) {
  const { title, tableCol, tableData, isDownloadReport, searchField } = props;

  waitForElement("#search_field", 3000).then(function () {
    const inputEl = document.getElementById("search_field");
    if (inputEl) inputEl.addEventListener(CHANGE, onChange);
  });

  window.addEventListener(LOAD, function () {
    if (tableCol?.find((col) => col?.field === ACTIONS)) {
      const download_icon = document.getElementById("download_icon");
      download_icon.addEventListener(CLICK, function () {
        GET_FILE("http://127.0.0.1:8000/getReport?id=pebblo_report_xhtml2pdf");
      });
    }
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
          (item) => /*html*/ `
            <tr class="table-row">
              ${tableCol?.myMap((col) =>
                Td({
                  children: col?.actions
                    ? col?.actions
                    : col?.render
                    ? col?.render(item)
                    : item[col?.field],
                  align: col?.align,
                  link:
                    col?.field !== ACTIONS && APP_DETAILS_ROUTE
                      ? `${APP_DETAILS_ROUTE}/?id=${APP_DATA?.instanceDetails?.id}`
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
    <div class="application-container flex flex-col gap-4">
      <div class="flex justify-between">
        <div class="inter surface-10 font-16 medium">${title}</div>
        <div class="flex">
          <div class="search">
            <input type="text" id="search_field" name="search" />
            <img
              src="${MEDIA_URL}/static/search-icon.png"
              alt="Search Icon" />
          </div>
       ${
         isDownloadReport
           ? /*html*/ `<div class="divider mt-2 mb-2 ml-4 mr-1"></div>
          ${Button({
            btnText: "Download Reports",
            startIcon: "/static/download-icon.png",
          })}`
           : ""
       }
        </div>
      </div>
      ${Table({
        tableCol: tableCol,
        tableData: tableData,
        link: APP_DETAILS_ROUTE,
      })}
  </div>
    `;
}
