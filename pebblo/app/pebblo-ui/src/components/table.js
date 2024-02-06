const APP_DATA = JSON.parse(document.scripts[0].getAttribute("appData"));

function Table(tableCol, tableData, link) {
  return `<table cellspacing="0" cellpadding="0">
    ${Thead(tableCol)}
    ${Tbody(tableCol, tableData, link)}
    </table>`;
}

function Thead(tableData) {
  return `
      <thead>${tableData
        ?.map((item) => {
          const className =
            item?.align === "start"
              ? "text-start"
              : item?.align === "center"
              ? "text-center"
              : "text-end";
          return `<th class="${className}">${item.label}</th>`;
        })
        .join("")}</thead>
    `;
}

function Tbody(tableCol, tableData, link) {
  return `
      <tbody>
      ${
        tableData?.length
          ? tableData
              ?.map(
                (item) =>
                  `<tr class="table-row">
           ${tableCol
             ?.map((col) =>
               Td(
                 col?.render ? col?.render(item) : item[col?.field],
                 col?.align,
                 col?.field !== "actions" && link
                   ? `${link}/?id=${APP_DATA?.instanceDetails?.id}`
                   : ""
               )
             )
             .join("")}
             </tr>`
              )
              .join("")
          : `<td class="pt-3 pb-3 pl-3 pr-3 text-center" colspan="5">No Data Found</td>`
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
    return `
      <td class="${className} pt-3 pb-3 pl-3 pr-3">
      ${children || "-"}
          <a href="${link}" id="link"><a/>
      </td>
   `;
  }
  return `
       <td class="${className} pt-3 pb-3 pl-3 pr-3">
       ${children || "-"}
       </td>
    `;
}

export { Table, Tbody, Thead, Td };
