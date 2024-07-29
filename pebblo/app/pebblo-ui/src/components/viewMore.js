import { Button, Dialog, Table } from "./index.js";
import { IDENTITY_TABLE_COL } from "../constants/constant.js";

export const ViewMore = (props) => {
  const {
    list,
    showCount,
    fileName,
    dialogTitle,
    id,
    showTooltip,
    tableCol,
    tableData,
    align = "start",
  } = props;
  const DialogBody = () => {
    return /*html*/ `
  <div class="load-history-table pt-6 pb-6 pr-6 pl-6 rounded-md">
   ${Table({ tableCol: tableCol, tableData: tableData })}
  </div>
  `;
  };

  return list && list.length > 0
    ? /*html*/ `
  <div class="flex items-center ${align === "end" ? "justify-end" : ""}">
    <div class="text-none">${list[0]}</div>
    ${
      list.length > 1
        ? Button({
            btnText: `+${list.length - 1}`,
            id: `identity-dialog-${id}-btn`,
          })
        : ""
    }
    ${
      list?.length > 1
        ? Dialog({
            title: dialogTitle,
            maxWidth: "md",
            dialogBody: DialogBody(),
            dialogId: `identity-dialog-${id}`,
            btnId: `identity-dialog-${id}-btn`,
          })
        : ""
    }
  </div>
`
    : "-";
};
