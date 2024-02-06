import { Button, Table } from "./index.js";

const MEDIA_URL = document.scripts[0].getAttribute("staticURL");

export function ApplicationsList(title, tableCol, tableData) {
  const navigateToDetailsPage = "/appDetails";
  document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchField")?.addEventListener("change", (e) => {
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
          ${filteredData
            ?.map(
              (item) => `
              <tr class="table-row">
                ${tableCol
                  ?.map((col) =>
                    Td(
                      col?.render ? col?.render(item) : item[col?.field],
                      col?.align,
                      col?.field !== "actions" && navigateToDetailsPage
                        ? `${navigateToDetailsPage}/?id=${APP_DATA?.instanceDetails?.id}`
                        : ""
                    )
                  )
                  .join("")}
              </tr>`
            )
            .join("")}
        `
        : ` <tr class="table-row">
               <td class="pt-3 pb-3 pl-3 pr-3 text-center" colspan="4">No Data Found</td>
            </tr>`;
    });
  });

  return `
    <div class="application-container flex flex-col gap-4">
    <div class="flex justify-between">
      <div class="inter surface-10 font-16 medium">${title}</div>
      <div class="flex">
        <div class="search">
          <input id="searchField" type="text" />
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
    ${Table(tableCol, tableData, navigateToDetailsPage)}
  </div>
    `;
}
