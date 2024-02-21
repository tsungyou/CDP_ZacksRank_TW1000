const { one_time_initialization_delete_no_rank_tickers, updateFile, readCSVFileToArray, checkZackLevelTickers } = require('./update_check');
const path = require('path');
const fs = require('fs');
// const c = api.getData('NVDA').then(console.log);

// const api = require('zacks-api');
// const data_example = {
//     ticker: 'NVDA',
//     name: 'NVIDIA Corporation',
//     zacksRankText: 'Buy',
//     zacksRank: '2',
//     updatedAt: '2024-02-13T04:22:00.000Z'
// }




//  =================================================================
const database_route = "../../Database/";
const yuanta_json = database_route + "zackRanks_yuanta.json";
const SP500_json = database_route + "zackRanks_SP500.json";
const NYSE_json = database_route + "zackRanks_NYSE.json";
const NASDAQ_json = database_route + "zackRanks_NASDAQ.json";
const portfolio = database_route + 'zackRanks_portfolio.json';
const closed_portfolio = database_route + 'zackRanks_closed.json';
// console.log("NYSE");
// updateFile(NYSE_json);
// console.log("SP500");
// updateFile(SP500_json);
// console.log("NASDAQ");
// updateFile(NASDAQ_json);
// console.log("Closed Port");
// updateFile(closed_portfolio);
// console.log("Port");
// updateFile(portfolio);
// console.log("Yuanta");
// updateFile(yuanta_json);
// //  =================================================================

console.log(":aaaa");
// const ib_list = ["C", "CCEP", "DSGX", "GGAL", "IBKR", "MU", "NDAQ", "NMIH", "SISI", "WFC"];
// const yuanta_list = ["SCHW", "XLB", "BMY", "NFLX", "XRX"];
// let array = [...ib_list, ...yuanta_list];

// const res = checkZackLevelTickers(NYSE_json);
// one_time_initialization_delete_no_rank_tickers(SP500_json);

// Call the asynchronous function
// api.getData('NVDA')
//     .then(data => {
//         // Inside this block, data will be the resolved value of the Promise
//         console.log(data.ticker); // This will print 'NVDA'
//     })
//     .catch(error => {
//         console.error('Error:', error.message);
//     });
