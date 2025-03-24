export function detectionColorStyle(symptomsList) {
    if (symptomsList.length === 0) {
        let theColors = {'background': 'var(--primary-color)', 'font': 'var(--secondary-color)'};
        return theColors
    }
    else {
        let topThresholdTag = '';
        for (let index in symptomsList) {
            if (topThresholdTag !== 'warningLevel') {
                let thresholdTag = symptomsList[index]['threshold_tag'];
                if (thresholdTag === 'LowerWarningLimit' || thresholdTag === 'UpperWarningLimit') {
                    topThresholdTag = 'warningLevel'
                }
                else {
                    topThresholdTag = 'cautionLevel'
                }
            }
        }
        if (topThresholdTag === 'warningLevel') {
            let theColors = {'background': '#3A0000', 'font': '#FF0000'};
            return theColors
        }
        else {
            let theColors = {'background': '#342E00', 'font': '#FFBF00'};
            return theColors
        }
    }
}

function dataframeToArray(df) {
    let array = [];
    for (let value in df) {
        if (df.hasOwnProperty(value)) {
            array.push(df[value])
        }
    }
    return array
}

function buildTrace(variable, values, xaxis, unit) {
    let trace = {};
    let variableName = variable + ' [' + unit + ']';
    if (values.hasOwnProperty(variable)) {
        let yaxis = dataframeToArray(values[variable]);
        trace = { x: xaxis, y: yaxis, mode: 'lines', name: variableName };
    }
    return trace
}

function buildThresholdTrace(xaxis, yval, the_color, the_style, the_name, the_bool) {
    let trace = {
        x: [xaxis[0], xaxis[xaxis.length - 1]],
        y: [yval, yval],
        name: the_name,
        showlegend: the_bool,
        mode: 'lines',
        line: {
            color: the_color,
            dash: the_style,
            width: 1,
        }};

    return trace
}
/*
function normalizeTrace(rawTrace, info) {
    // Prse input
    let variable = rawTrace['name'];
    let nominal = info[variable]['nominal'];
    let y = rawTrace['y'];
    // Create auxiliar variables
    let newy = [];
    let yy = 0;
    // Normalize
    for (let index in y) {
        let epsilon = 0.0000000001;
        nominal = Math.max(nominal, epsilon); // To avoid zero division
        yy = 100 * (y[index] - nominal) / nominal;
        newy.push(yy);
    }
    rawTrace['y'] = newy;
    return rawTrace
}
*/
function buildRange(plotData, variable, variableName, telemetryInfo) {
    let variableIndex = 0;
    for (let index in plotData) {
        let traceInfo = plotData[index];
        if (traceInfo['name'] === variable) {
            variableIndex = index;
        }
    }

    let yaxis = plotData[variableIndex]['y'];
    let lastValue = yaxis[yaxis.length - 1];

    let upperLimit = telemetryInfo[variableName]['high_warning_threshold'];
    let lowerLimit = telemetryInfo[variableName]['low_warning_threshold'];

    let upperRange = Math.max(lastValue, upperLimit);
    let lowerRange = Math.min(lastValue, lowerLimit);
    let delta = upperRange - lowerRange;
    let margin = 0.05 * delta;
    let range = [lowerRange - margin, upperRange + margin];

    return range
}


let red = 'rgba(255,0,0,0.8)';
let orange = 'rgba(196,126,0,0.8)';

// colors for graph
let blue = 'rgba(0, 0, 255, 0.8)';
let lightblue = 'rgba(0, 128, 255, 0.8)';
let darkblue = 'rgba(0, 0, 153, 0.8)';
let green = 'rgba(0, 255, 0, 0.8)';
let lightgreen = 'rgba(128, 255, 0, 0.8)';
let darkgreen = 'rgba(0, 153, 0, 0.8)';
let yellow = 'rgba(255, 255, 0, 0.8)';
let lightyellow = 'rgba(255, 255, 153, 0.8)';
let darkyellow = 'rgba(153, 153, 0, 0.8)';
let violet = 'rgba(153, 52, 255, 0.8)';
let lightviolet = 'rgba(178, 102, 255, 0.8)';
let darkviolet = 'rgba(102, 0, 102, 0.8)';
let pink = 'rgba(255, 0, 127, 0.8)';
let lightpink = 'rgba(255, 153, 204, 0.8)';
let darkpink = 'rgba(153, 0, 76, 0.8)';

let colors = [blue, green, yellow, violet, pink, lightblue, lightgreen, lightyellow, lightviolet, lightpink,
    darkblue, darkgreen, darkyellow, darkviolet, darkpink];

let gridblue = 'rgba(0, 0, 255, 0.2)';
let gridlightblue = 'rgba(0, 128, 55, 0.2)';
let griddarkblue = 'rgba(0, 0, 153, 0.2)';
let gridgreen = 'rgba(0, 255, 0, 0.2)';
let gridlightgreen = 'rgba(128, 255, 0, 0.2)';
let griddarkgreen = 'rgba(0, 153, 0, 0.2)';
let gridyellow = 'rgba(255, 255, 0, 0.2)';
let gridlightyellow = 'rgba(255, 255, 153, 0.2)';
let griddarkyellow = 'rgba(153, 153, 0, 0.2)';
let gridviolet = 'rgba(153, 52, 255, 0.2)';
let gridlightviolet = 'rgba(178, 102, 255, 0.2)';
let griddarkviolet = 'rgba(102, 0, 102, 0.2)';
let gridpink = 'rgba(255, 0, 127, 0.2)';
let gridlightpink = 'rgba(255, 153, 204, 0.2)';
let griddarkpink = 'rgba(153, 0, 76, 0.2)';

let gridcolors = [gridblue, gridgreen, gridyellow, gridviolet, gridpink, gridlightblue, gridlightgreen, gridlightyellow,
    gridlightviolet, gridlightpink, griddarkblue, griddarkgreen, griddarkyellow, griddarkviolet, griddarkpink];


export function processedPlotData(telemetryDict, selectedVariables) {
    // Parse de jsoned dataframe to a javascript object
    let values = JSON.parse(telemetryDict['values']);
    let info = JSON.parse(telemetryDict['info']);
    let selectedVariablesUnits = {};
    for (let index in selectedVariables) {
        let variable = selectedVariables[index];
        let units = info[variable]['units'];
        selectedVariablesUnits[variable] = units;
    }

    // Build a time array for the xaxis
    let xaxis = [];
    for (let i = 0; i < 60; i++) {
        let stamp = i - 59;
        xaxis.push(stamp.toString());
    }

    // Build the processed data according to the number of selected variables
    let processedData = [];

    // If only one variable is selected, display its absolute value and all its associated thresholds
    if (selectedVariables.length === 1) {
        let variable = selectedVariables[0];

        // Build main trace
        let trace = buildTrace(variable, values, xaxis, selectedVariablesUnits[variable]);
        // trace['line'] = {color: pink};
        processedData.push(trace);

        // Build threshold and nominal traces
        trace = buildThresholdTrace(xaxis, info[variable]['low_warning_threshold'], red, 'dot', 'Warning Limits', true);
        processedData.push(trace);
        trace = buildThresholdTrace(xaxis, info[variable]['low_caution_threshold'], orange, 'dot', 'Caution Limits', true);
        processedData.push(trace);
        // trace = buildThresholdTrace(xaxis, info[variable]['nominal'], blue, 'dot', 'Nominal value', true);
        // processedData.push(trace);
        trace = buildThresholdTrace(xaxis, info[variable]['high_caution_threshold'], orange, 'dot', 'Caution Limits', false);
        processedData.push(trace);
        trace = buildThresholdTrace(xaxis, info[variable]['high_warning_threshold'], red, 'dot', 'Warning Limits', false);
        processedData.push(trace);
    }
    /*else if (selectedVariables.length === 2) {
        // If two variables are selected, display only its absolute values with two different vertical axis
        let trace = {};

        // Build first variable trace
        trace = buildTrace(selectedVariables[0], values,  xaxis);
        // trace['line'] = {color: pink};
        processedData.push(trace);

        // Build second variable trace
        trace = buildTrace(selectedVariables[1], values,  xaxis);
        // trace['line'] = {color: green};
        trace['yaxis'] = 'y2';
        processedData.push(trace);

    }*/
    else {
        // If two variables are selected, display only its absolute values with two different vertical axis
        let trace = {};
        let colorIndex = 0;
        let axisIndex = 1;
        let axisName = '';
        for (let index in selectedVariables) {
            if (axisIndex != 1) {
                axisName = 'y' + axisIndex;
            } else {
                axisName = 'y';
            }
            let units = selectedVariablesUnits[selectedVariables[index]];
            trace = buildTrace(selectedVariables[index], values, xaxis, units);

            if (colorIndex == colors.length - 1) {
                colorIndex = 0;
            }
            trace['line'] = {color: colors[colorIndex]};
            trace['yaxis'] = axisName;
            processedData.push(trace);
            axisIndex++;
            colorIndex++;
        }
    }

    return processedData
}

export function setLayout(selectedVariables, telemetryInfo, plotData) {
    let selectedVariablesUnits = {};
    for (let index in selectedVariables) {
        let variable = selectedVariables[index];
        let units = telemetryInfo[variable]['units'];
        selectedVariablesUnits[variable] = units;
    }

    let layout = {
        autosize: true,
        margin: {l: 35, r: 10, b: 25, t: 20, pad: 0},
        showlegend: true,
        legend: {orientation: 'h', font: {family: 'sans-serif', size: 12, color: 'var(--color__text)'}},
        plot_bgcolor: '#111111',
        paper_bgcolor: '#111111',
        xaxis: {
            tickcolor: 'var(--color__text)',
            showgrid: false,
            domain: [0, 4],
        },
        yaxis: {
            side: 'left',
            titlefont: {color: 'var(--color__text)',},
            tickfont: {color: 'var(--color__text)',},
            tickcolor: 'var(--color__text)',
            gridcolor: 'var(--color__text)',
            linecolor: 'var(--color__text)',
            anchor:'free',
            position: 0.01,
        }
    };

    if (selectedVariables.length === 1) {
        //let variable = selectedVariables[0];
        //let units = selectedVariablesUnits[variable];
        //let label = variable + ' [' + units + ']';
        //layout['yaxis']['title'] = label;
    }
    /*else if (selectedVariables.length === 2) {
        //layout['margin']['r'] = 60;
        layout['xaxis']['domain'] = [0.05, 1.05];
        let variableLeft = selectedVariables[0];
        //let unitsLeft = selectedVariablesUnits[variableLeft];
        //let labelLeft = variableLeft + ' [' + unitsLeft + ']';

        let variableRight = selectedVariables[1];
        //let unitsRight = selectedVariablesUnits[variableRight];
        //let labelRight = variableRight + ' [' + unitsRight + ']';

        //layout['yaxis']['title'] = labelLeft;
        layout['yaxis']['range'] = buildRange(plotData, variableLeft, telemetryInfo);

        layout['yaxis2'] = JSON.parse(JSON.stringify(layout['yaxis']));
        //layout['yaxis2']['title'] = labelRight;
        layout['yaxis2']['range'] = buildRange(plotData, variableRight, telemetryInfo);
        layout['yaxis2']['side'] = 'left';
        layout['yaxis2']['overlaying'] = 'y';
        layout['yaxis2']['position'] = 0.05;

        layout['showlegend'] = true;
    }*/
    else if (selectedVariables.length > 1) {
        let colorIndex = 0;
        let axisIndex = 1;
        let axisName = '';
        let currentVariable = selectedVariables[0];
        let shift = 0.04;
        for (let i = 0; i < selectedVariables.length; i++) {
            currentVariable = selectedVariables[i];
            let currentVariableWithUnits = currentVariable + ' [' + selectedVariablesUnits[currentVariable] + ']';
            if (i == 0) {
                axisName = 'yaxis';
                layout[axisName]['range'] = buildRange(plotData, currentVariableWithUnits, currentVariable, telemetryInfo);
            }
            else {
                axisName = 'yaxis' + axisIndex;
                layout[axisName] = JSON.parse(JSON.stringify(layout['yaxis']));
                layout[axisName]['range'] = buildRange(plotData, currentVariableWithUnits, currentVariable, telemetryInfo);
                layout[axisName]['overlaying'] = 'y';
                layout[axisName]['position'] = shift*i + 0.01;
            }

            if (colorIndex == colors.length - 1) {
                colorIndex = 0;
            }

            layout[axisName]['tickfont'] = {color: colors[colorIndex]};
            layout[axisName]['tickcolor'] = colors[colorIndex];
            layout[axisName]['gridcolor'] = gridcolors[colorIndex];
            layout[axisName]['linecolor'] = gridcolors[colorIndex];

            colorIndex++;
            axisIndex++;
        }
        layout['xaxis']['domain'] = [0.01+shift*(selectedVariables.length-1), 1];
        layout['showlegend'] = true;
    }

    return layout
}

function markChildrenObtainNonChildrenIndex(procedure, stepIndex, checkThis) {
    // Retrieve and parse some useful information for comfort
    let totalSteps = procedure['procedureSteps'].length;
    let currentDepth = procedure['procedureSteps'][stepIndex]['depth'];

    // Initialize the iteration variable, the loop condition and an index to store the non-children position,
    let nonChildrenIndex = -1;
    let i = stepIndex;
    let foundNonChildren = false;

    // Loop. Note that this while always breaks because we reach the end of the array at some point.
    while (!foundNonChildren) {
        // Update the counter
        i += 1;
        // If the iteration variable is outside range, switch the loop condition (to break the while, although we
        // actually haven't found a non-children)
        if (i >= totalSteps) {break}
        else {
            // Retrieve next step depth
            let nextDepth = procedure['procedureSteps'][i]['depth'];
            // Check if it's a non children (non-children have equal or minor depth)
            if (nextDepth <= currentDepth) {
                foundNonChildren = true;
                nonChildrenIndex = i;
            }
            else {
                procedure['procedureSteps'][i]['isDone'] = checkThis;
            }
        }
    }

    return [procedure, nonChildrenIndex]
}

function uncheckAfterNonChildren(procedure, nonChildrenIndex) {
    let foundNonChildren = (nonChildrenIndex !== -1);
    let totalSteps = procedure['procedureSteps'].length;

    if (foundNonChildren) {
        for (let j = nonChildrenIndex; j < totalSteps; j++) {
            procedure['procedureSteps'][j]['isDone'] = false;
        }
    }
    return procedure
}

function checkAllExceptContainers(procedure, stepIndex, depthLimit) {
    let isFirstOfThisDepthArray = [true, true, true];
    if (stepIndex > 0) {
        for (let j = stepIndex - 1; j >= 0; j--) {
            // Retrieve step depth
            let thisDepth = procedure['procedureSteps'][j]['depth'];
            // Build the condition bools (for readability)
            let isFirstOfThisDepth = isFirstOfThisDepthArray[thisDepth];
            let hasMinorDepth = (thisDepth < depthLimit);
            // Mark as checked or unchecked depending on the conditions
            if (isFirstOfThisDepth && hasMinorDepth) {
                procedure['procedureSteps'][j]['isDone'] = false;
                isFirstOfThisDepthArray[thisDepth] = false;
            }
            else {
                procedure['procedureSteps'][j]['isDone'] = true;
            }
        }
    }
    return procedure
}

function checkTheBox(procedure, stepIndex) {
    // If we are in this function, that can only happen if we are checking a box that was previously unchecked.
    // 1) All the following steps that are not "children steps" HAVE TO BE UNCHECKED.
    //    1.1) We loop forward, we check all children and we find the first step that is not a children (if any).
    //    1.2) We loop from such step onwards and we mark all of them as unchecked.
    // 2) Note that, from 1.1), we know which is the next step that is not a children. Refer to it as X.
    //    2.1) If X doesn't exist, then the procedure is finished and all steps should be checked. We can loop backwards
    //         from the current step and mark all of them as finished.
    //    2.2) If X exists, let D be its depth (which is for sure equal or minor than the current depth, since by
    //         construction, it's not a children).
    //         2.2.1) All the previous steps should be checked except the ones that "contain" our current step.
    //                That is, we can loop backwards and mark all steps as checked except those which satisfy:
    //                2.3.1) They have a minor depth than the current non-children step
    //                AND
    //                2.3.2) They are the first steps of their own depth that we find while looping backwards.

    // Check the current step
    procedure['procedureSteps'][stepIndex]['isDone'] = true;
    let nonChildrenIndex;

    // Set children to the same status and find first non-children index (step 1.1)
    [procedure, nonChildrenIndex] = markChildrenObtainNonChildrenIndex(procedure, stepIndex, true);
    let foundNonChildren = (nonChildrenIndex !== -1);

    // Mark all steps after the first non-children as unchecked (1.2)
    procedure = uncheckAfterNonChildren(procedure, nonChildrenIndex);

    // If X doesn't exist, loop backwards and mark all steps as checked (2.1)
    if (!foundNonChildren) {
        if (stepIndex > 0) {
            for (let j = stepIndex - 1; j >= 0; j--) {
                procedure['procedureSteps'][j]['isDone'] = true;
            }
        }
    }

    // If X exists, define its depth (2.2)
    let nonChildrenDepth = -1;
    if (foundNonChildren) {
        nonChildrenDepth = procedure['procedureSteps'][nonChildrenIndex]['depth'];

        // Loop backwards and mark every step as checked except the ones that meet the said conditions (2.2.1)
        procedure = checkAllExceptContainers(procedure, stepIndex, nonChildrenDepth);
    }

    return procedure
}

function uncheckTheBox(procedure, stepIndex) {
    // If we are in this function, that can only happen if we are unchecking a box that was previously checked.
    // 1) All the following steps that are not "children steps" HAVE TO BE UNCHECKED.
    //    1.1) We loop forward, we check all children and we find the first step that is not a children (if any).
    //    1.2) We loop from such step onwards and we mark all of them as unchecked.
    // 2) All the previous steps should be checked except the ones that "contain" our current step.
    //    That is, we can loop backwards and mark all steps as checked except those which satisfy:
    //    2.1) They have a minor depth than the current step
    //    AND
    //    2.2) They are the first steps of their own depth that we find while looping backwards.

    // Uncheck the current step
    procedure['procedureSteps'][stepIndex]['isDone'] = false;
    let nonChildrenIndex;

    // Set children to the same status and find first non-children index (step 1.1)
    [procedure, nonChildrenIndex] = markChildrenObtainNonChildrenIndex(procedure, stepIndex, false);

    // Mark all steps after the first non-children as unchecked (1.2)
    procedure = uncheckAfterNonChildren(procedure, nonChildrenIndex);

    // Loop backwards and mark every step as checked except the ones that meet the said conditions (2.2.1)
    let currentDepth = procedure['procedureSteps'][stepIndex]['depth'];
    procedure = checkAllExceptContainers(procedure, stepIndex, currentDepth);

    return procedure
}

export function updateCheckboxes(procedureDict, stepIndex) {
    // Make a local copy of the argument. The name 'Dict' appendix is avoided for comfort
    let procedure = JSON.parse(JSON.stringify(procedureDict));

    // Local bool variable indicating whether the step box is checked or not (before update)
    let isChecked = procedure['procedureSteps'][stepIndex]['isDone'];
    let checkThisBox = !isChecked;
    procedure['procedureSteps'][stepIndex]['isDone'] = !isChecked;

    // Depending on whether the step box is being checked or not, check or uncheck its parent step boxes
    // if (checkThisBox) {procedure = checkTheBox(procedure, stepIndex)}
    // else {procedure = uncheckTheBox(procedure, stepIndex)}

    // Return the updated procedure dictionary
    return procedure
}
