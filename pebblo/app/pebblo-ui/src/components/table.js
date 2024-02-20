import { get_Text_Orientation } from "../util.js";
import { ACTIONS } from "../constants/enums.js";
import { Tooltip } from "./tooltip.js";

function Table(props) {
  const { tableCol, tableData, link } = props;
  return /*html*/ `
  <table cellspacing="0" cellpadding="0">
    ${Thead(tableCol)}
    ${Tbody(tableCol, tableData, link)}
   </table>`;
}

function Thead(tableCol) {
  return /*html*/ `
      <thead>${tableCol?.myMap((item) => {
        const TEXT__ALIGN = get_Text_Orientation(item?.align);
        return `<th class="${TEXT__ALIGN}">${item.label}</th>`;
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
             Td({
               children: col?.actions
                 ? col?.actions
                 : col?.render
                 ? col?.render(item)
                 : item[col?.field],
               align: col?.align,
               link:
                 col?.field !== ACTIONS && link
                   ? `${link}/?id=${item?.loadId}`
                   : "",
               maxWidth: col?.type === "label" ? "text-ellipsis" : "fit",
             })
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

function Td(props) {
  const { children, align, link, maxWidth } = props;
  const TEXT__ALIGN = get_Text_Orientation(align);
  if (link) {
    return /*html*/ `
      <td class="${TEXT__ALIGN} capitalize pt-3 pb-3 pl-3 pr-3 ${maxWidth}">
      ${children || "-"}
          <a href="${link}" id="link"></a>
      </td>
   `;
  }
  return `
    <td class="${TEXT__ALIGN} capitalize pt-3 pb-3 pl-3 pr-3 ${maxWidth}">
       ${children || "-"}
       </td>
    `;
}

export { Table, Tbody, Thead, Td };
