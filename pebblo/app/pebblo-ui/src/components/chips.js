import { Button, Dialog, Table } from "./index.js";
import { IDENTITY_TABLE_COL } from "../constants/constant.js";

export const Chips = (props) => {
  const { list, showCount, fileName, dialogTitle } = props;
  const btnId = fileName ? fileName.split("/").at(-1).split(".").at(0) : "1";

  const DialogBody = () => {
    const TABLE_DATA = list.map((identityName) => ({ identity: identityName }));
    return /*html*/ `
  <div class="load-history-table pt-6 pb-6 pr-6 pl-6 rounded-md">
   ${Table({ tableCol: IDENTITY_TABLE_COL, tableData: TABLE_DATA })}
  </div>
  `;
  };

  return list && list.length > 0
    ? /*html*/ `
  <div class="flex items-center w-fit">
    <div>${list[0]}</div>
    ${Button({
      btnText: `+${list.length - 1}`,
      id: `identity-dialog-${btnId}-btn`,
    })}
    ${Dialog({
      title: dialogTitle,
      maxWidth: "md",
      dialogBody: DialogBody(),
      dialogId: `identity-dialog-${btnId}`,
      btnId: `identity-dialog-${btnId}-btn`,
    })}
  </div>
`
    : "-";
};
