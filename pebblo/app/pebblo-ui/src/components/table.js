import { APP_DATA } from "../constants/constant.js";

function Table(tableCol, tableData, link) {
  return /*html*/ `<table cellspacing="0" cellpadding="0">
    ${Thead(tableCol)}
    ${Tbody(tableCol, tableData, link)}
    </table>`;
}

function Thead(tableCol) {
  return /*html*/ `
      <thead>${tableCol?.myMap((item) => {
        const className =
          item?.align === "start"
            ? "text-start"
            : item?.align === "center"
            ? "text-center"
            : "text-end";
        return `<th class="${className}">${item.label}</th>`;
      })}</thead>
    `;
}

function Tbody(tableCol, tableData, link) {
  return /*html*/ `
      <tbody>
      ${
        tableData?.length
          ? tableData?.myMap(
              (item) => /*html*/ `<tr class="table-row">
           ${tableCol?.myMap((col) =>
             Td(
               col?.render ? col?.render(item) : item[col?.field],
               col?.align,
               col?.field !== "actions" && link
                 ? `${link}/?id=${APP_DATA?.instanceDetails?.id}`
                 : ""
             )
           )}
             </tr>`
            )
          : /*html*/ `<td class="pt-3 pb-3 pl-3 pr-3 text-center" colspan="${
              tableCol?.length + 1
            }">No Data Found</td>`
      }
      </tbody>
    `;
}

function Td(children, align, link) {
  const className =
    align === "start"
      ? "text-start"
      : align === "center"
      ? "text-center"
      : "text-end";

  if (link) {
    return /*html*/ `
      <td class="${className} pt-3 pb-3 pl-3 pr-3">
      ${children || "-"}
          <a href="${link}" id="link"><a/>
      </td>
   `;
  }
  return /*html*/ `
       <td class="${className} pt-3 pb-3 pl-3 pr-3">
       ${children || "-"}
       </td>
    `;
}

export { Table, Tbody, Thead, Td };
