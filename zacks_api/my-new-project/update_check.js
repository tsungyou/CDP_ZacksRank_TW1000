const api = require('zacks-api');
const fs = require('fs');
function formatDate(data){
    return data.split('T')[0];
}

// const readJsonFileToArray = (filePath) => {
//     let existingData = {};
//     try{
//         existingData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
//     } catch (error) {
//         console.error('Error reading existing data:', error);
//     }
//     return Object.keys(existingData);

// }

const updateFile = (filePath) => {
    
    let existingData = {};

    try{
        existingData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    } catch (error) {
        console.error('Error reading existing data:', error);
    }
    const array = Object.keys(existingData);
    console.log(array);
    Promise.all(array.map(symbol => api.getData(symbol)))
        .then(datas => {
            const modify_list = [];
            datas.forEach(data => {
                try {
                    const ticker = data.ticker;
                    // console.log(ticker);
                    const updatedAt = formatDate(data.updatedAt);
                    const zacksRank = data.zacksRank;
        
                    // Organize data
                    if (!existingData[ticker]) {
                        existingData[ticker] = {};
                    }
                    const ranks =  existingData[ticker];
                    if (ranks) {
        
                        const lastRank = Object.values(ranks);
                        const lastValue = lastRank[lastRank.length - 1];
        
                        // console.log(lastValue, ticker);
                        if (zacksRank != lastValue) {
                            modify_list.push(`${ticker}: ${lastValue} => ${zacksRank}.`);
                        }
                        existingData[ticker][updatedAt] = zacksRank;
                        
                        
                    }
                } catch (error) {
                    // console.log(symbol);
                    console.error('Error:', error.message, symbol);
                    
                }});
                
            if (modify_list.length > 0) console.log(modify_list); else console.log("no changes are made"); 
            // Write organized data to data.json
            fs.writeFile(filePath, JSON.stringify(existingData, null, 2), err => {
                if (err) {
                    console.error('Error writing to file:', err);
                    return;
                }
                console.log('Data has been written to', filePath);
            });
        })
        .catch(error => {
            console.error('Error fetching Zacks data:', error.message);
            // console.log(data);
        });
}


function readCSVFileToArray(filePath) {
    // Read the CSV file
    const fileContent = fs.readFileSync(filePath, 'utf-8');

    // Split the content into rows
    const rows = fileContent.split('\n');

    // Initialize an array to store the data
    const dataArray = [];

    // Process each row
    rows.forEach(row => {
        // Split the row into columns
        const columns = row.split(',')[0];

        // Add the columns to the data array
        dataArray.push(columns);
    });
    const cleanedStrings = dataArray.map(str => str.replace(/\r$/, ''));
    return cleanedStrings;
}

// check zack level tickers
const checkZackLevelTickers = (spPath) => {
    let one = [];
    let two = [];
    let four = [];
    let five = [];
    let list_ = {};
    const level = "1";
    const level2 = "2";
    const level4 = "4";
    const level5 = "5";
    try { 
        list_ = JSON.parse(fs.readFileSync(spPath, 'utf8'));
    } catch (error) {
        console.error('Error reading existing data:', error);
    }
    // let list_ = {  DVA: { '2024-02-13': '2' },
    // RL: { '2024-02-13': '1' },
    // VFC: { '2024-02-13': '4' },
    // MHK: { '2024-02-13': '4' },
    // FOX: { '2024-02-13': '' },
    // NWS: { '2024-02-13': '' },
    // GPS: { '2024-02-13': '1' }};
    for (const key in list_) {
        const lastKey = Object.keys(list_[key]).pop();
        // console.log(lastKey);
        if (list_[key][lastKey] === level){
            one.push(key);
        } else if (list_[key][lastKey] === level2) {
            two.push(key);
        } else if (list_[key][lastKey] === level4) {
            four.push(key);
        } else if (list_[key][lastKey] === level5) {
            five.push(key);
        }
    }
    return {
        one,
        two,
        four,
        five
    };
};

const one_time_initialization_delete_no_rank_tickers = (path) => {
    let list_ = {};
    try { 
        list_ = JSON.parse(fs.readFileSync(path, 'utf8'));
    } catch (error) {
        console.error('Error reading existing data:', error);
    }
    for (const key in list_) {
        const lastKey = Object.keys(list_[key]).pop();
        // console.log(lastKey);
        if (list_[key][lastKey] === ""){
            delete list_[key];
            console.log(key);
        }
    }
    fs.writeFileSync(path, JSON.stringify(list_, null, 2));
}
module.exports = { one_time_initialization_delete_no_rank_tickers, updateFile, readCSVFileToArray, checkZackLevelTickers, };
