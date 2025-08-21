"""
BioSim Configuration Templates

This module contains XML templates for different types of BioSim simulations.
Each template can be customized with specific parameters like duration, malfunctions, etc.
"""

# Base BioSim configuration template
BASE_BIOSIM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<biosim xmlns="http://www.traclabs.com/biosim"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.traclabs.com/biosim ../../schema/BiosimInitSchema.xsd">
    <Globals driverStutterLength="1000"
        crewsToWatch="IHab_Group"
        runTillCrewDeath="false" runTillN="{max_ticks}" startPaused="false" tickLength="0.1">
    </Globals>
    <SimBioModules>
        <environment>
            <SimEnvironment moduleName="IHab" initialVolume="22900" />
            <SimEnvironment moduleName="HALO" initialVolume="22900" />
        </environment>
        <air>
            <NitrogenStore capacity="10000"
                moduleName="Nitrogen_Store" level="10000">
            </NitrogenStore>
            <VCCR moduleName="Main_VCCR" logLevel="INFO">
                <powerConsumer inputs="General_Power_Store"
                    desiredFlowRates="340" maxFlowRates="1000" ></powerConsumer>
                <airConsumer inputs="IHab"
                    desiredFlowRates="10000" maxFlowRates="10000"></airConsumer>
                <airProducer desiredFlowRates="10000"
                    outputs="IHab" maxFlowRates="10000" />
                <CO2Producer desiredFlowRates="10000" outputs="CO2_Store"
                    maxFlowRates="10000"></CO2Producer>
                {vccr_malfunction}
            </VCCR>
            <OGS moduleName="OGS">
                <powerConsumer inputs="General_Power_Store"
                    desiredFlowRates="1000" maxFlowRates="1000" />
                <potableWaterConsumer inputs="Potable_Water_Store"
                    desiredFlowRates="10" maxFlowRates="10" />
                <O2Producer desiredFlowRates="1000" outputs="O2_Store"
                    maxFlowRates="1000"></O2Producer>
                <H2Producer desiredFlowRates="1000" outputs="H2_Store"
                    maxFlowRates="1000" />
            </OGS>
            <O2Store capacity="10000" moduleName="O2_Store"
                level="1000">
            </O2Store>
            <H2Store capacity="10000" moduleName="H2_Store" level="0"></H2Store>
            <CO2Store capacity="1000" moduleName="CO2_Store"
                level="0">
            </CO2Store>
        </air>
        <framework>
            <Injector moduleName="Oxygen_Injector_IHab">
                <O2Consumer inputs="O2_Store" desiredFlowRates="0.195"
                    maxFlowRates="0.195" >
                </O2Consumer>
                <O2Producer desiredFlowRates="0.195"
                    outputs="IHab" maxFlowRates="0.195" >
                </O2Producer>
            </Injector>
        </framework>
        <water>
            <WaterRS moduleName="Water_Distiller"
                implementation="LINEAR">
                <powerConsumer inputs="General_Power_Store"
                    desiredFlowRates="1000" maxFlowRates="1000" ></powerConsumer>
                <dirtyWaterConsumer inputs="Dirty_Water_Store"
                    desiredFlowRates="10" maxFlowRates="10">
                </dirtyWaterConsumer>
                <greyWaterConsumer inputs="Grey_Water_Store"
                    desiredFlowRates="10" maxFlowRates="10" />
                <potableWaterProducer desiredFlowRates="1000"
                    outputs="Potable_Water_Store" maxFlowRates="1000" />
            </WaterRS>
            <DirtyWaterStore capacity="1000"
                moduleName="Dirty_Water_Store" level="0">
            </DirtyWaterStore>
            <GreyWaterStore capacity="1000"
                moduleName="Grey_Water_Store" level="0">
            </GreyWaterStore>
            <PotableWaterStore capacity="1000"
                moduleName="Potable_Water_Store" level="1000">
            </PotableWaterStore>
        </water>
        <power>
            <PowerStore capacity="100000"
                moduleName="General_Power_Store" level="100000">
            </PowerStore>
            <PowerPS moduleName="General_Power_Producer"
                generationType="NUCLEAR" upperPowerGeneration="500000">
                <powerProducer desiredFlowRates="1000000"
                    outputs="General_Power_Store" maxFlowRates="1000000" />
            </PowerPS>
        </power>
        <food>
            <FoodStore capacity="10000" level="10000"
                moduleName="Food_Store">
            </FoodStore>
        </food>
        <waste>
            <DryWasteStore capacity="1000000"
                moduleName="Dry_Waste_Store" level="0">
            </DryWasteStore>
        </waste>
        <crew>
            <CrewGroup moduleName="IHab_Group">
                <potableWaterConsumer inputs="Potable_Water_Store"
                    desiredFlowRates="3" maxFlowRates="3">
                </potableWaterConsumer>
                <airConsumer inputs="IHab" desiredFlowRates="0"
                    maxFlowRates="0" />
                <foodConsumer inputs="Food_Store" desiredFlowRates="5"
                    maxFlowRates="5">
                </foodConsumer>
                <dirtyWaterProducer desiredFlowRates="100"
                    outputs="Dirty_Water_Store" maxFlowRates="100">
                </dirtyWaterProducer>
                <greyWaterProducer desiredFlowRates="100"
                    outputs="Grey_Water_Store" maxFlowRates="100" />
                <airProducer desiredFlowRates="0" outputs="IHab"
                    maxFlowRates="0" />
                <dryWasteProducer desiredFlowRates="10"
                    outputs="Dry_Waste_Store" maxFlowRates="10">
                </dryWasteProducer>
                <crewPerson age="35" name="Test_Crew" sex="FEMALE"
                    weight="55">
                    <schedule>
                        <activity intensity="2" name="ruminating"
                            length="12" />
                        <activity intensity="0" name="sleep" length="8" />
                        <activity intensity="5" name="exercise"
                            length="2" />
                    </schedule>
                </crewPerson>
            </CrewGroup>
        </crew>
    </SimBioModules>
    <Sensors>
        <environment>
            <GasPressureSensor input="IHab" moduleName="ppCO2_IHab" gasType="CO2">
                <alarms>
                    <warning_high min="0.5999507" max="0.799934"/>
                    <critical_high min="0.799934" max="100"/>
                </alarms>
                <normalStochasticFilter deviation="0.005"/>
            </GasPressureSensor>
            <GasPressureSensor input="IHab" moduleName="ppO2_IHab" gasType="O2">
                <alarms>
                    <critical_low min="0" max="19"/>
                    <warning_low min="19" max="20.665"/>
                    <warning_high min="23.3314" max="24.6646"/>
                    <critical_high min="24.6646" max="4000"/>
                </alarms>
                <normalStochasticFilter deviation="0.005"/>
            </GasPressureSensor>
            <GasConcentrationSensor input="IHab" moduleName="Humidity_IHab" gasType="VAPOR">
                <alarms>
                    <critical_low min="0" max="0.40"/>
                    <warning_low min="0.40" max="0.50"/>
                    <warning_high min="0.61" max="0.70"/>
                    <critical_high min="0.70" max="1.00"/>
                </alarms>
                <normalStochasticFilter deviation="0.005"/>
            </GasConcentrationSensor>
            <TotalPressureSensor input="IHab" moduleName="Total_Cabin_Pressure_IHab">
                <alarms>
                    <critical_low min="0" max="87.56342"/>
                    <warning_low min="87.56342" max="100.31872"/>
                    <warning_high min="102.7319" max="104.8003"/>
                    <critical_high min="102.7319" max="104.8003"/>
                </alarms>
                <normalStochasticFilter deviation="0.005"/>
            </TotalPressureSensor>
        </environment>
    </Sensors>
</biosim>"""

# Malfunction templates for different anomaly types
MALFUNCTION_TEMPLATES = {
    'CO₂ Scrubber Valve Leak': {
        'description': 'VCCR CO2 scrubber valve malfunction causing CO2 buildup',
        'vccr_malfunction': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="200"/>',
        'affected_systems': ['VCCR', 'CO2_Store', 'ppCO2_IHab']
    },
    'CO2 Scrubber Valve Leak': {
        'description': 'VCCR CO2 scrubber valve malfunction causing CO2 buildup',
        'vccr_malfunction': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="200"/>',
        'affected_systems': ['VCCR', 'CO2_Store', 'ppCO2_IHab']
    },
    'Fan Bearing Wear': {
        'description': 'VCCR fan bearing degradation affecting air circulation',
        'vccr_malfunction': '<malfunction intensity="MEDIUM_MALF" length="PERMANENT_MALF" occursAtTick="200"/>',
        'affected_systems': ['VCCR', 'air circulation', 'ppCO2_IHab']
    },
    'Absorption Bed Saturated': {
        'description': 'VCCR absorption bed saturation reducing CO2 removal efficiency',
        'vccr_malfunction': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="200"/>',
        'affected_systems': ['VCCR', 'CO2_Store', 'ppCO2_IHab']
    },
    'Heater Coil Failure': {
        'description': 'VCCR heater coil malfunction affecting temperature control',
        'vccr_malfunction': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="200"/>',
        'affected_systems': ['VCCR', 'temperature control', 'ppCO2_IHab']
    }
}

# Default malfunction template for unknown anomalies
DEFAULT_MALFUNCTION = {
    'description': 'Generic VCCR malfunction',
    'vccr_malfunction': '<malfunction intensity="MEDIUM_MALF" length="PERMANENT_MALF" occursAtTick="200"/>',
    'affected_systems': ['VCCR', 'general systems']
}

def get_malfunction_config(anomaly_name: str) -> dict:
    """
    Get malfunction configuration for a specific anomaly.
    
    Args:
        anomaly_name: Name of the anomaly
        
    Returns:
        Dictionary containing malfunction configuration
    """
    # Try exact match first
    if anomaly_name in MALFUNCTION_TEMPLATES:
        return MALFUNCTION_TEMPLATES[anomaly_name]
    
    # Try partial matches
    for key, config in MALFUNCTION_TEMPLATES.items():
        if key.lower() in anomaly_name.lower() or anomaly_name.lower() in key.lower():
            return config
    
    # Return default if no match found
    return DEFAULT_MALFUNCTION

def generate_config(anomaly_name: str, duration_seconds: int) -> str:
    """
    Generate complete BioSim configuration for an anomaly.
    
    Args:
        anomaly_name: Name of the anomaly to simulate
        duration_seconds: Duration of the simulation in seconds
        
    Returns:
        Complete XML configuration string
    """
    # Get malfunction configuration
    malfunction_config = get_malfunction_config(anomaly_name)
    
    # Calculate max ticks based on duration
    # BioSim runs at 0.1 second intervals, so duration_seconds * 10 = ticks
    max_ticks = int(duration_seconds * 10)
    
    # Format the configuration
    config_content = BASE_BIOSIM_TEMPLATE.format(
        max_ticks=max_ticks,
        vccr_malfunction=malfunction_config['vccr_malfunction']
    )
    
    return config_content
