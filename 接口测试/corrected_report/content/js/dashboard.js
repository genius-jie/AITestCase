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

    var data = {"OkPercent": 36.36363636363637, "KoPercent": 63.63636363636363};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.36363636363636365, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.0, 500, 1500, "边界值-history文本为单字符"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度接近上限"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-正常对话（问题类）"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度中间值"], "isController": false}, {"data": [1.0, 500, 1500, "无效输入-history为空数组"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪+搜索组合"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-负面情绪"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-视觉意图（Bug：应返回VISION）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图不匹配（问题类）"], "isController": false}, {"data": [0.5, 500, 1500, "有效输入-中性情绪"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图不匹配（Bug：应返回RECOMMEND）"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-情绪与意图匹配（Bug：应返回VISION）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪+记忆组合（Bug：应返回MEMORY_WRITE）"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-悲伤情绪"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度下限"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-情绪+视觉组合（Bug：应返回VISION）"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-情绪与意图匹配（Bug：应返回MEMORY_WRITE）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-记忆写入意图（Bug：应返回MEMORY_WRITE）"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度接近下限"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-开心情绪"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-推荐意图（Bug：应返回RECOMMEND）"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-asr_emotion为空字符串"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪+意图组合（Bug：应返回RECOMMEND）"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-情绪与意图匹配"], "isController": false}, {"data": [1.0, 500, 1500, "有效输入-生气情绪"], "isController": false}, {"data": [1.0, 500, 1500, "无效输入-history参数缺失"], "isController": false}, {"data": [1.0, 500, 1500, "边界值-asr_emotion_confidence缺失"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-多轮对话"], "isController": false}, {"data": [0.0, 500, 1500, "有效输入-搜索意图"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-置信度上限"], "isController": false}, {"data": [1.0, 500, 1500, "边界值-history中role无效"], "isController": false}, {"data": [0.0, 500, 1500, "边界值-history文本为空字符串"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 33, 21, 63.63636363636363, 66.78787878787875, 12, 256, 63.0, 78.6, 133.4999999999995, 256.0, 11.811023622047244, 7.783839253758053, 4.274295924302076], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["边界值-history文本为单字符", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.34672619047619, 5.347842261904762], "isController": false}, {"data": ["边界值-置信度接近上限", 1, 1, 100.0, 77.0, 77, 77, 77.0, 77.0, 77.0, 77.0, 12.987012987012989, 9.334415584415584, 4.527698863636363], "isController": false}, {"data": ["有效输入-正常对话（问题类）", 1, 1, 100.0, 256.0, 256, 256, 256.0, 256.0, 256.0, 256.0, 3.90625, 2.811431884765625, 1.392364501953125], "isController": false}, {"data": ["边界值-置信度中间值", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.592741935483872, 5.607358870967742], "isController": false}, {"data": ["无效输入-history为空数组", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 12.01923076923077, 23.963341346153847], "isController": false}, {"data": ["有效输入-情绪+搜索组合", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.71875, 6.174395161290323], "isController": false}, {"data": ["有效输入-负面情绪", 1, 0, 0.0, 72.0, 72, 72, 72.0, 72.0, 72.0, 72.0, 13.888888888888888, 10.077582465277779, 4.828559027777779], "isController": false}, {"data": ["有效输入-视觉意图（Bug：应返回VISION）", 1, 1, 100.0, 65.0, 65, 65, 65.0, 65.0, 65.0, 65.0, 15.384615384615385, 11.057692307692307, 5.4387019230769225], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（问题类）", 1, 1, 100.0, 64.0, 64, 64, 64.0, 64.0, 64.0, 64.0, 15.625, 11.3525390625, 5.9814453125], "isController": false}, {"data": ["有效输入-中性情绪", 2, 1, 50.0, 62.5, 62, 63, 62.5, 63.0, 63.0, 63.0, 2.967359050445104, 2.140033846439169, 1.0577012240356083], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（Bug：应返回RECOMMEND）", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.486235119047619, 6.122891865079365], "isController": false}, {"data": ["有效输入-情绪与意图匹配（Bug：应返回VISION）", 1, 0, 0.0, 72.0, 72, 72, 72.0, 72.0, 72.0, 72.0, 13.888888888888888, 10.036892361111112, 5.520290798611112], "isController": false}, {"data": ["有效输入-情绪+记忆组合（Bug：应返回MEMORY_WRITE）", 1, 1, 100.0, 77.0, 77, 77, 77.0, 77.0, 77.0, 77.0, 12.987012987012989, 9.423193993506494, 4.667207792207792], "isController": false}, {"data": ["有效输入-悲伤情绪", 1, 0, 0.0, 67.0, 67, 67, 67.0, 67.0, 67.0, 67.0, 14.925373134328359, 10.80048973880597, 5.188899253731343], "isController": false}, {"data": ["边界值-置信度下限", 1, 1, 100.0, 78.0, 78, 78, 78.0, 78.0, 78.0, 78.0, 12.82051282051282, 9.227263621794872, 4.457131410256411], "isController": false}, {"data": ["有效输入-情绪+视觉组合（Bug：应返回VISION）", 1, 0, 0.0, 61.0, 61, 61, 61.0, 61.0, 61.0, 61.0, 16.393442622950822, 11.910860655737705, 6.179559426229508], "isController": false}, {"data": ["有效输入-情绪与意图匹配（Bug：应返回MEMORY_WRITE）", 1, 0, 0.0, 64.0, 64, 64, 64.0, 64.0, 64.0, 64.0, 15.625, 11.2762451171875, 5.889892578125], "isController": false}, {"data": ["有效输入-记忆写入意图（Bug：应返回MEMORY_WRITE）", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.34672619047619, 5.704365079365079], "isController": false}, {"data": ["边界值-置信度接近下限", 1, 1, 100.0, 64.0, 64, 64, 64.0, 64.0, 64.0, 64.0, 15.625, 11.23046875, 5.4473876953125], "isController": false}, {"data": ["有效输入-开心情绪", 1, 0, 0.0, 77.0, 77, 77, 77.0, 77.0, 77.0, 77.0, 12.987012987012989, 9.385146103896105, 4.553064123376624], "isController": false}, {"data": ["有效输入-推荐意图（Bug：应返回RECOMMEND）", 1, 1, 100.0, 79.0, 79, 79, 79.0, 79.0, 79.0, 79.0, 12.658227848101266, 9.110462816455696, 4.4748813291139244], "isController": false}, {"data": ["边界值-asr_emotion为空字符串", 1, 1, 100.0, 75.0, 75, 75, 75.0, 75.0, 75.0, 75.0, 13.333333333333334, 9.544270833333334, 4.557291666666667], "isController": false}, {"data": ["有效输入-情绪+意图组合（Bug：应返回RECOMMEND）", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.486235119047619, 6.029885912698413], "isController": false}, {"data": ["有效输入-情绪与意图匹配", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.71875, 6.174395161290323], "isController": false}, {"data": ["有效输入-生气情绪", 1, 0, 0.0, 81.0, 81, 81, 81.0, 81.0, 81.0, 81.0, 12.345679012345679, 8.957851080246913, 4.328221450617284], "isController": false}, {"data": ["无效输入-history参数缺失", 1, 0, 0.0, 12.0, 12, 12, 12.0, 12.0, 12.0, 12.0, 83.33333333333333, 21.891276041666668, 25.797526041666668], "isController": false}, {"data": ["边界值-asr_emotion_confidence缺失", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.833705357142858, 24.623325892857142], "isController": false}, {"data": ["有效输入-多轮对话", 1, 1, 100.0, 62.0, 62, 62, 62.0, 62.0, 62.0, 62.0, 16.129032258064516, 11.529737903225806, 8.91507056451613], "isController": false}, {"data": ["有效输入-搜索意图", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.377728174603174, 5.657862103174603], "isController": false}, {"data": ["边界值-置信度上限", 1, 1, 100.0, 65.0, 65, 65, 65.0, 65.0, 65.0, 65.0, 15.384615384615385, 11.057692307692307, 5.3485576923076925], "isController": false}, {"data": ["边界值-history中role无效", 1, 0, 0.0, 20.0, 20, 20, 20.0, 20.0, 20.0, 20.0, 50.0, 7.91015625, 17.7734375], "isController": false}, {"data": ["边界值-history文本为空字符串", 1, 1, 100.0, 63.0, 63, 63, 63.0, 63.0, 63.0, 63.0, 15.873015873015872, 11.331225198412698, 5.33234126984127], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Emotion mismatch. Expected: 关切, Actual: 平淡", 6, 28.571428571428573, 18.181818181818183], "isController": false}, {"data": ["Emotion mismatch. Expected: 愤怒, Actual: 关切", 1, 4.761904761904762, 3.0303030303030303], "isController": false}, {"data": ["Label mismatch. Expected: SEARCH, Actual: CHAT", 2, 9.523809523809524, 6.0606060606060606], "isController": false}, {"data": ["Label mismatch. Expected: CHAT, Actual: SEARCH", 12, 57.142857142857146, 36.36363636363637], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 33, 21, "Label mismatch. Expected: CHAT, Actual: SEARCH", 12, "Emotion mismatch. Expected: 关切, Actual: 平淡", 6, "Label mismatch. Expected: SEARCH, Actual: CHAT", 2, "Emotion mismatch. Expected: 愤怒, Actual: 关切", 1, "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": ["边界值-history文本为单字符", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度接近上限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-正常对话（问题类）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度中间值", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-情绪+搜索组合", 1, 1, "Label mismatch. Expected: SEARCH, Actual: CHAT", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-视觉意图（Bug：应返回VISION）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（问题类）", 1, 1, "Label mismatch. Expected: SEARCH, Actual: CHAT", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-中性情绪", 2, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪与意图不匹配（Bug：应返回RECOMMEND）", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-情绪+记忆组合（Bug：应返回MEMORY_WRITE）", 1, 1, "Emotion mismatch. Expected: 愤怒, Actual: 关切", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["边界值-置信度下限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-记忆写入意图（Bug：应返回MEMORY_WRITE）", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度接近下限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-推荐意图（Bug：应返回RECOMMEND）", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-asr_emotion为空字符串", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪+意图组合（Bug：应返回RECOMMEND）", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-情绪与意图匹配", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["有效输入-多轮对话", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["有效输入-搜索意图", 1, 1, "Emotion mismatch. Expected: 关切, Actual: 平淡", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["边界值-置信度上限", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["边界值-history文本为空字符串", 1, 1, "Label mismatch. Expected: CHAT, Actual: SEARCH", 1, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
