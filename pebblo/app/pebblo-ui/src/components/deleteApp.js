import { DeleteIcon } from "../icons/index.js";
import { showSnackbar } from "../services/snackbar.js";
import { Button, Dialog } from "../components/index.js";
import { CLICK, LOAD } from "../constants/enums.js";
import { DELETE_APP_ROUTE } from "../constants/routesConstant.js";
import { DELETE_APP } from "../services/delete.js";

const SUCCESS_CODE = 200;

export const DeleteAppButton = (props) => {
  const appName = props?.appName || "";
  const redirectAfterDelete = props?.redirectRoute || "";
  const DeleteAppDialogBody = () => {
    window.addEventListener(LOAD, function () {
      const delete_icon = document.getElementById("delete_confirm_btn");
      const DIALOG = document.getElementById("delete_app_dialog");
      delete_icon?.addEventListener(CLICK, async function () {
        const res = await DELETE_APP(`${DELETE_APP_ROUTE}?app_name=${appName}`);
        if (res?.status === SUCCESS_CODE) {
          DIALOG.close();
          showSnackbar("App deleted successfully", () => {
            window.location.href = redirectAfterDelete;
          });
        } else {
          DIALOG.close();
          showSnackbar("Failed to delete app");
        }
      });
    });

    return /*html*/ `
         <div>
          <div class="flex flex-col gap-1">
            <div class="font-14 inter">Are you sure you want to delete this app?</div>
          </div>
          <div class="text-right">
            ${Button({
              class: "ml-auto",
              id: `delete_confirm_btn`,
              variant: "contained",
              btnText: "Confirm",
              color: "critical",
            })}
          </div>
         </div>
        `;
  };
  return `<div> ${Button({
    variant: "text",
    btnText: "Delete App",
    startIcon: DeleteIcon({ color: "critical" }),
    id: "delete_app_btn",
    color: "critical",
  })}
   ${Dialog({
     title: "Delete App",
     maxWidth: "sm",
     dialogBody: DeleteAppDialogBody(),
     dialogId: "delete_app_dialog",
     btnId: "delete_app_btn",
   })}
  </div>`;
};
