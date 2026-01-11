/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 33.333333333333336, "KoPercent": 66.66666666666667};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.3333333333333333, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.0, 500, 1500, "边界值-history文本为单字符"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度接近上限"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图不匹配（Bug：应返回SEARCH）"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度中间值"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪+搜索组合（Bug：应返回SEARCH）"], "isController": false}, {"data": [1.0, 500, 1500, "无效输入-history为空数组"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-负面情绪"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-视觉意图（Bug：应返回VISION）"], "isController": false}, {"data": [0.5, 500, 1500, "有效输入-中性情绪"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图不匹配（Bug：应返回RECOMMEND）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图匹配（Bug：应返回VISION）"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-情绪+记忆组合（Bug：应返回MEMORY_WRITE）"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-悲伤情绪"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度下限"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-情绪+视觉组合（Bug：应返回VISION）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图匹配（Bug：应返回MEMORY_WRITE）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-记忆写入意图（Bug：应返回MEMORY_WRITE）"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度接近下限"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-开心情绪"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-推荐意图（Bug：应返回RECOMMEND）"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-asr_emotion为空字符串"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-搜索意图（Bug：应返回SEARCH）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪+意图组合（Bug：应返回RECOMMEND）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图匹配"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-生气情绪"], "isController": false}, {"data": [1.0, 500, 1500, "无效输入-history参数缺失"], "isController": false}, {"data": [1.0, 500, 1500, "边界值-asr_emotion_confidence缺失"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-正常对话"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-多轮对话"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度上限"], "isController": false}, {"data": [1.0, 500, 1500, "边界值-history中role无效"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-history文本为空字符串"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 33, 22, 66.66666666666667, 61.48484848484847, 10, 130, 62.0, 76.6, 115.99999999999994, 130.0, 12.336448598130842, 8.127190420560748, 4.464442172897196], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["边界值-history文本为单字符", 1, 1, 100.0, 74.0, 74, 74, 74.0, 74.0, 74.0, 74.0, 13.513513513513514, 9.646853885135135, 4.552892736486487], "isController": false}, {"data": ["边界值-置信度接近上限", 1, 1, 100.0, 61.0, 61, 61, 61.0, 61.0, 61.0, 61.0, 16.393442622950822, 11.766777663934427, 5.715292008196721], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（Bug：应返回SEARCH）", 1, 1, 100.0, 60.0, 60, 60, 60.0, 60.0, 60.0, 60.0, 16.666666666666668, 12.076822916666668, 6.380208333333334], "isController": false}, {"data": ["边界值-置信度中间值", 1, 1, 100.0, 74.0, 74, 74, 74.0, 74.0, 74.0, 74.0, 13.513513513513514, 9.726034628378379, 4.6980574324324325], "isController": false}, {"data": ["有效输入-情绪+搜索组合（Bug：应返回SEARCH）", 1, 1, 100.0, 60.0, 60, 60, 60.0, 60.0, 60.0, 60.0, 16.666666666666668, 12.093098958333334, 6.380208333333334], "isController": false}, {"data": ["无效输入-history为空数组", 1, 0, 0.0, 11.0, 11, 11, 11.0, 11.0, 11.0, 11.0, 90.9090909090909, 14.204545454545455, 28.3203125], "isController": false}, {"data": ["有效输入-负面情绪", 1, 0, 0.0, 130.0, 130, 130, 130.0, 130.0, 130.0, 130.0, 7.6923076923076925, 5.581430288461538, 2.6742788461538463], "isController": false}, {"data": ["有效输入-视觉意图（Bug：应返回VISION）", 1, 1, 100.0, 76.0, 76, 76, 76.0, 76.0, 76.0, 76.0, 13.157894736842104, 9.444387335526317, 4.651521381578948], "isController": false}, {"data": ["有效输入-中性情绪", 2, 1, 50.0, 61.0, 61, 61, 61.0, 61.0, 61.0, 61.0, 2.941176470588235, 2.1197150735294117, 1.0483685661764706], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（Bug：应返回RECOMMEND）", 1, 1, 100.0, 65.0, 65, 65, 65.0, 65.0, 65.0, 65.0, 15.384615384615385, 11.1328125, 5.9344951923076925], "isController": false}, {"data": ["有效输入-情绪与意图匹配（Bug：应返回VISION）", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.671496975806452, 6.410660282258065], "isController": false}, {"data": ["有效输入-情绪+记忆组合（Bug：应返回MEMORY_WRITE）", 1, 0, 0.0, 60.0, 60, 60, 60.0, 60.0, 60.0, 60.0, 16.666666666666668, 12.076822916666668, 5.989583333333334], "isController": false}, {"data": ["有效输入-悲伤情绪", 1, 0, 0.0, 65.0, 65, 65, 65.0, 65.0, 65.0, 65.0, 15.384615384615385, 11.1328125, 5.3485576923076925], "isController": false}, {"data": ["边界值-置信度下限", 1, 1, 100.0, 60.0, 60, 60, 60.0, 60.0, 60.0, 60.0, 16.666666666666668, 11.979166666666668, 5.794270833333334], "isController": false}, {"data": ["有效输入-情绪+视觉组合（Bug：应返回VISION）", 1, 0, 0.0, 76.0, 76, 76, 76.0, 76.0, 76.0, 76.0, 13.157894736842104, 9.547183388157896, 4.959909539473684], "isController": false}, {"data": ["有效输入-情绪与意图匹配（Bug：应返回MEMORY_WRITE）", 1, 1, 100.0, 77.0, 77, 77, 77.0, 77.0, 77.0, 77.0, 12.987012987012989, 9.372463474025974, 4.89549512987013], "isController": false}, {"data": ["有效输入-记忆写入意图（Bug：应返回MEMORY_WRITE）", 1, 1, 100.0, 61.0, 61, 61, 61.0, 61.0, 61.0, 61.0, 16.393442622950822, 11.71875, 5.891393442622951], "isController": false}, {"data": ["边界值-置信度接近下限", 1, 1, 100.0, 61.0, 61, 61, 61.0, 61.0, 61.0, 61.0, 16.393442622950822, 11.782786885245901, 5.715292008196721], "isController": false}, {"data": ["有效输入-开心情绪", 1, 0, 0.0, 72.0, 72, 72, 72.0, 72.0, 72.0, 72.0, 13.888888888888888, 10.023328993055557, 4.869249131944445], "isController": false}, {"data": ["有效输入-推荐意图（Bug：应返回RECOMMEND）", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.608492943548388, 5.701864919354839], "isController": false}, {"data": ["边界值-asr_emotion为空字符串", 1, 1, 100.0, 58.0, 58, 58, 58.0, 58.0, 58.0, 58.0, 17.241379310344826, 12.341729525862068, 5.893049568965517], "isController": false}, {"data": ["有效输入-搜索意图（Bug：应返回SEARCH）", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.377728174603174, 5.657862103174603], "isController": false}, {"data": ["有效输入-情绪+意图组合（Bug：应返回RECOMMEND）", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.671496975806452, 6.127142137096774], "isController": false}, {"data": ["有效输入-情绪与意图匹配", 1, 1, 100.0, 61.0, 61, 61, 61.0, 61.0, 61.0, 61.0, 16.393442622950822, 11.92686987704918, 6.275614754098361], "isController": false}, {"data": ["有效输入-生气情绪", 1, 0, 0.0, 69.0, 69, 69, 69.0, 69.0, 69.0, 69.0, 14.492753623188406, 10.51573822463768, 5.080955615942028], "isController": false}, {"data": ["无效输入-history参数缺失", 1, 0, 0.0, 10.0, 10, 10, 10.0, 10.0, 10.0, 10.0, 100.0, 26.26953125, 30.95703125], "isController": false}, {"data": ["边界值-asr_emotion_confidence缺失", 1, 0, 0.0, 10.0, 10, 10, 10.0, 10.0, 10.0, 10.0, 100.0, 26.3671875, 34.47265625], "isController": false}, {"data": ["有效输入-正常对话", 1, 1, 100.0, 110.0, 110, 110, 110.0, 110.0, 110.0, 110.0, 9.09090909090909, 6.551846590909091, 3.2404119318181817], "isController": false}, {"data": ["有效输入-多轮对话", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.51398689516129, 8.91507056451613], "isController": false}, {"data": ["边界值-置信度上限", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.408730158730158, 5.518353174603175], "isController": false}, {"data": ["边界值-history中role无效", 1, 0, 0.0, 10.0, 10, 10, 10.0, 10.0, 10.0, 10.0, 100.0, 15.8203125, 35.546875], "isController": false}, {"data": ["边界值-history文本为空字符串", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.51398689516129, 5.418346774193548], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Emotion mismatch. Expected: 关切, Actual: 平淡", 4, 18.181818181818183, 12.121212121212121], "isController": false}, {"data": ["Label mismatch. Expected: CHAT, Actual: SEARCH", 14, 63.63636363636363, 42.42424242424242], "isController": false}, {"data": ["Emotion mismatch. Expected: 关切, Actual: 悲伤", 4, 18.181818181818183, 12.121212121212121], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 33, 22, "Label mismatch. Expected: CHAT, Actual: SEARCH", 14, "Emotion mismatch. Expected: 关切, Actual: 平淡", 4, "Emotion mismatch. Expected: 关切, Actual: 悲伤", 4, "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": ["边界值-history文本为单字符", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度接近上限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（Bug：应返回SEARCH）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 悲伤", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度中间值", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪+搜索组合（Bug：应返回SEARCH）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 悲伤", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-视觉意图（Bug：应返回VISION）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-中性情绪", 2, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（Bug：应返回RECOMMEND）", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪与意图匹配（Bug：应返回VISION）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 悲伤", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["边界值-置信度下限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-情绪与意图匹配（Bug：应返回MEMORY_WRITE）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 悲伤", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-记忆写入意图（Bug：应返回MEMORY_WRITE）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度接近下限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-推荐意图（Bug：应返回RECOMMEND）", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-asr_emotion为空字符串", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-搜索意图（Bug：应返回SEARCH）", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪+意图组合（Bug：应返回RECOMMEND）", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪与意图匹配", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-正常对话", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-多轮对话", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度上限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["边界值-history文本为空字符串", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
