const uploadButton = document.querySelector("#upload-button") as HTMLButtonElement;
const inputFile = document.querySelector("#upload-file") as HTMLInputElement;
const statusDisplay = document.querySelector("#upload-status") as HTMLParagraphElement;


const API_URL = import.meta.env.VITE_API_URL as string;

uploadButton.addEventListener("click", async (event)=>{
  event.preventDefault();
  uploadButton.disabled = true;
  statusDisplay.textContent = "";
  if(!inputFile.files || inputFile.files.length === 0){
    statusDisplay.textContent = "ファイルを選択してください";
    //後で赤くするようなクラスをつけてもいいかも
    uploadButton.disabled = false;
    return;
  }
  console.log(inputFile);
  console.log(inputFile.files[0])
  const file = inputFile.files[0];
  const formData = new FormData();
  formData.append("file", file);
  try{
    const response = await fetch(API_URL, {
      method:"POST",
      body: formData
    });
    if(!response.ok){
      throw new Error(`HTTP Error: ${response.status} - ${response.statusText}`);
    }
    const result = await response.json();
    console.log(result)
    statusDisplay.textContent = "成功";
  }
  catch(error){
    console.error(String(error));
    statusDisplay.textContent = "アップロードに失敗しました";
  }
  finally{
    uploadButton.disabled = false;
  }
});