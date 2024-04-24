import { SORT_DATA, getTextOrientation, waitForElement } from "../util.js";
import { ACTIONS, ACTIVE, ASC, CLICK, DSC, LOAD } from "../constants/enums.js";
import { Tooltip } from "./tooltip.js";
import { StraightIcon } from "../icons/index.js";

// PROPS {
//   tableCol: Array<unknown>,
//   tableData: Array<unknown>,
//   link?: string,
//   isSorting: boolean,
// }

function Table(props) {
  const { tableCol, tableData, link, isSorting } = props;
  if (isSorting) {
    waitForElement("#search_field", 1000).then(function () {
      let sortedData = tableData;
      const table_head = document.getElementsByClassName("sort-column");
      Array.from(table_head).forEach((el) => {
        el.addEventListener(CLICK, () => {
          Array.from(table_head).forEach((th) => {
            th.classList.remove("active");
            th.classList.remove(ASC);
            th.classList.remove(DSC);
          });
          el.classList.add("active");
          el.classList.add(el.dataset.order);
          sortedData = SORT_DATA(
            tableData,
            el.dataset.order,
            el.dataset.column
          );
          document.getElementsByTagName("tbody")[0].innerHTML = TABLE_BODY({
            tableCol,
            tableData: sortedData,
            link,
          });
          el.dataset.order = el.dataset.order === ASC ? DSC : ASC;
        });
      });
    });
  }

  return /*html*/ `
  <table cellspacing="0" cellpadding="0">
    ${Thead({ tableCol, isSorting })}
    ${Tbody({ tableCol, tableData, link })}
   </table>`;
}

// PROPS {
//   tableCol: Array<unknown>,
//   isSorting?: boolean
// }

function Thead(props) {
  const { tableCol, isSorting } = props;
  return /*html*/ `
      <thead>${tableCol?.myMap((col) => {
        const TEXT__ALIGN = getTextOrientation(col?.align);
        return /*html*/ `<th class="${TEXT__ALIGN} ${
          !isSorting || col?.field === ACTIONS
            ? ""
            : "cursor-pointer sort-column"
        }" data-column="${col?.field}" data-order="${DSC}">
              ${
                !isSorting || col?.field === ACTIONS
                  ? col.label
                  : /*html*/ `<div class="flex gap-1 items-center ${TEXT__ALIGN}">
              ${StraightIcon({ color: "grey", size: "sm" })}
              <div>${col.label}</div>
              </div>`
              }
        </th>`;
      })}</thead>
    `;
}

function Tbody(props) {
  return /*html*/ `
      <tbody>
         ${TABLE_BODY(props)}
      </tbody>
    `;
}

// PROPS {
//   children: string | HTMLElement,
//   align?: string,
//   link?: string,
//   isTooltip?: boolean,
//   tooltipTitle?: string,
// }

function Td(props) {
  const {
    children,
    align = "start",
    link,
    isTooltip,
    tooltipTitle,
    tooltipWidth,
    id,
  } = props;
  const TEXT__ALIGN = getTextOrientation(align);
  let td;
  if (link) {
    waitForElement(`#link-${id}`, 500)
      .then(function () {
        const TdID = document.getElementById(`link-${id}`);
        TdID.addEventListener(CLICK, (event) => {
          event.stopPropagation();
          window.location = link;
        });
      })
      .catch((e) => {
        console.log(e);
      });
    td = /*html*/ `
      <td class="${TEXT__ALIGN} capitalize pt-3 pb-3 pl-3 pr-3 fit" id="link-${id}">
      ${children || "-"}
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
    <td class="${TEXT__ALIGN} capitalize pt-3 pb-3 pl-3 pr-3 ${
      tooltipWidth ? tooltipWidth : "text-ellipsis"
    }">
       ${Tooltip({
         children: children || "-",
         title: tooltipTitle,
       })}
       </td>
    `;
  }
  return td;
}

// PROPS {
//   tableCol: Array<unknown>,
//   tableData: Array<unknown>,
//   link?: string,
// }

const TABLE_BODY = (props) => {
  const { tableCol, tableData, link } = props;
  return tableData?.length
    ? tableData?.myMap(
        (item, index) => /*html*/ `<tr class="table-row ">
   ${tableCol?.myMap((col, itemIndex) =>
     Td({
       children: col?.render ? col?.render(item) : item[col?.field],
       align: col?.align,
       link:
         col?.field !== ACTIONS && link ? `${link}?app_name=${item?.name}` : "",
       isTooltip: col?.tooltipTitle ? col?.tooltipTitle(item) : "",
       tooltipTitle: col?.tooltipTitle ? col?.tooltipTitle(item) : "",
       tooltipWidth: col?.tooltipWidth,
       id: `${index}-${itemIndex}`,
     })
   )}
     </tr>`
      )
    : /*html*/ `<td class="pt-3 pb-3 pl-3 pr-3 text-center" colspan="${
        tableCol?.length + 1
      }">No Data Found</td>`;
};

export { Table, Tbody, Thead, Td };
