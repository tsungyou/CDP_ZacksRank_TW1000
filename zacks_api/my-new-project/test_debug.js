let currentDate = new Date();

currentDate.setDate(currentDate.getDate() - 1);

// console.log(currentDate);

let test = new Date();


// console.log(test);

console.log(formatDate());
function formatDate(){
    let date = new Date();

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const dat = String(date.getDate() - 1).padStart(2, '0'); 
    return `${year}-${month}-${dat}`;
}