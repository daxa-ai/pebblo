import { MEDIA_URL } from "../constants/constant.js";
import { Button, Table, Td } from "./index.js";

export function ApplicationsList(props) {
  const { title, tableCol, tableData, isDownloadReport } = props;
  const APP_DETAILS_ROUTE = "/appDetails";
  window.addEventListener("load", function () {
    const inputEl = document.getElementById("search_field");
    if (inputEl) inputEl.addEventListener("change", onChange);
  });

  function onChange(e) {
    let filteredData;
    if (e.target.value) {
      filteredData = tableData?.filter((item) =>
        item?.application
          ?.toLocaleLowerCase()
          ?.includes(e.target.value.toLocaleLowerCase())
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
                Td(
                  col?.render ? col?.render(item) : item[col?.field],
                  col?.align,
                  col?.field !== "actions" && APP_DETAILS_ROUTE
                    ? `${APP_DETAILS_ROUTE}/?id=1234`
                    : ""
                )
              )}
            </tr>`
        )}
      `
      : /*html*/ ` <tr class="table-row">
             <td class="pt-3 pb-3 pl-3 pr-3 text-center" colspan="4">No Data Found</td>
          </tr>`;
  }

  return /*html*/ `
    <div class="application-container flex flex-col gap-4">
      <div class="flex justify-between">
        <div class="inter surface-10 font-16 medium">${title}</div>
        <div class="flex">
          <div class="search">
            <input id="search_field" type="text" />
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
      ${Table(tableCol, tableData, APP_DETAILS_ROUTE)}
  </div>
    `;
}
