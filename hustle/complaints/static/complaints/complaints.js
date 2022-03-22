let reimburseButton = document.getElementById("reimburse_button");
let reimbursementInfo = document.getElementById("reimbursement_info");

let confirmReimburseButton = document.getElementById("confirmReimbursementButton");
let cancelReimburseButton = document.getElementById("cancelReimburseButton");

if (reimburseButton != null) {
    reimburseButton.addEventListener("click", function() {
        if (reimbursementInfo.style.display == 'none') {
            reimbursementInfo.style.display = 'block';
        }
    })
}

cancelReimburseButton.addEventListener("click", function() {
    if (reimbursementInfo.style.display == "block") {
        reimbursementInfo.style.display == "none";
    }
})