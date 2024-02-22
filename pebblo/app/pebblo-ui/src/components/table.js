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
                 ? col?.actions(item)
                 : col?.render
                 ? col?.render(item)
                 : item[col?.field],
               align: col?.align,
               link:
                 col?.field !== ACTIONS && link
                   ? `${link}/?app_name=${item?.name}`
                   : "",
               isTooltip: col?.isTooltip,
               tooltipTitle: col?.tooltipTitle ? col?.tooltipTitle(item) : "",
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
  const { children, align, link, isTooltip, tooltipTitle } = props;
  const TEXT__ALIGN = get_Text_Orientation(align);
  let td;
  if (link) {
    td = /*html*/ `
      <td class="${TEXT__ALIGN} capitalize pt-3 pb-3 pl-3 pr-3 fit">
      ${children || "-"}
          <a href="${link}" id="link"></a>
      </td>
   `;
  } else {
    td = /*html*/ `
    <td class="${TEXT__ALIGN} capitalize pt-3 pb-3 pl-3 pr-3 fit">
       ${children || "-"}
       </td>
    `;
  }
  if (isTooltip) {
    return /*html*/ `
    <td class="${TEXT__ALIGN} capitalize pt-3 pb-3 pl-3 pr-3 text-ellipsis">
       ${Tooltip({
         children: children || "-",
         title: tooltipTitle,
       })}
       </td>
    `;
  }
  return td;
}

export { Table, Tbody, Thead, Td };
