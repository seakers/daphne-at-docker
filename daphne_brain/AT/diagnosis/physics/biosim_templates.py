"""
BioSim Configuration Templates

This module contains XML templates for different types of BioSim simulations.
Each template can be customized with specific parameters like duration, malfunctions, etc.
"""

from typing import List, Dict, Union
import itertools

# Base BioSim configuration template
BASE_BIOSIM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="../../style/table.xsl"?>
<biosim xmlns="http://www.traclabs.com/biosim"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.traclabs.com/biosim ../../schema/BiosimInitSchema.xsd">
	<Globals driverStutterLength="0"
		crewsToWatch="IHab_Group"
		runTillCrewDeath="false" runTillN="{max_ticks}" startPaused="false" tickLength="0.1">
	</Globals>
	<SimBioModules>
		<environment>
			<SimEnvironment moduleName="IHab" initialVolume="22900"> 
			</SimEnvironment>
			<SimEnvironment moduleName="HALO" initialVolume="22900" />
			<Dehumidifier moduleName="Main_Dehumidifier">
				<airConsumer inputs="IHab"
					desiredFlowRates="0.3" maxFlowRates="0.3"></airConsumer>
				<dirtyWaterProducer desiredFlowRates="10000"
					outputs="Dirty_Water_Store" maxFlowRates="10000" />
			</Dehumidifier>
			<Fan moduleName="IHab_to_HALO_Fan">
				<airConsumer inputs="IHab"
					desiredFlowRates="40" maxFlowRates="40" />
				<powerConsumer inputs="General_Power_Store"
					desiredFlowRates="9000" maxFlowRates="9000" ></powerConsumer>
				<airProducer desiredFlowRates="40"
					outputs="HALO" maxFlowRates="40" ></airProducer>
			</Fan>
			<Fan moduleName="HALO_to_IHab_Fan">
				<airConsumer inputs="HALO"
					desiredFlowRates="40" maxFlowRates="40" />
				<powerConsumer inputs="General_Power_Store" desiredFlowRates="50"
					maxFlowRates="50"></powerConsumer>
				<airProducer desiredFlowRates="40"
					outputs="IHab" maxFlowRates="40" ></airProducer>
			</Fan>
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
				<O2Consumer inputs="O2_Store" desiredFlowRates="0.0"
					maxFlowRates="0.0" >
				</O2Consumer>
				<O2Producer desiredFlowRates="0.0"
					outputs="IHab" maxFlowRates="0.0" >
				</O2Producer>
			</Injector>
			<Injector moduleName="Oxygen_Injector_HALO">
				<O2Consumer inputs="O2_Store" desiredFlowRates="0.0"
					maxFlowRates="0.0" >
				</O2Consumer>
				<O2Producer desiredFlowRates="0.0"
					outputs="HALO" maxFlowRates="0.0" >
				</O2Producer>
			</Injector>
			<Injector moduleName="Nitrogen_Injector_HALO">
				<nitrogenConsumer inputs="Nitrogen_Store" desiredFlowRates="0.0"
					maxFlowRates="0.0" >
				</nitrogenConsumer>
				<nitrogenProducer desiredFlowRates="0.0"
					outputs="HALO" maxFlowRates="0.0" >
				</nitrogenProducer>
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
				<crewPerson age="35" name="Wilma Deering" sex="FEMALE"
					weight="55">
					<schedule>
						<activity intensity="2" name="ruminating"
							length="12" />
						<activity intensity="0" name="sleep" length="8" />
						<activity intensity="5" name="excercise"
							length="2" />
					</schedule>
				</crewPerson>
				<crewPerson age="35" name="Tim O'Connor" sex="MALE"
					weight="72">
					<schedule>
						<activity intensity="2" name="ruminating"
							length="12" />
						<activity intensity="0" name="sleep" length="8" />
						<activity intensity="5" name="excercise"
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
					<warning_high min="0.25" max="0.35"/>
					<critical_high min="0.35" max="100"/>
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
					<critical_high min="104.8003" max="110" />
				</alarms>
				<normalStochasticFilter deviation="0.005"/>
			</TotalPressureSensor>
			<GasPressureSensor input="HALO" moduleName="ppCO2_HALO" gasType="CO2">
				<alarms>
					<warning_high min="0.25" max="0.35"/>
					<critical_high min="0.35" max="100"/>
				</alarms>
				<normalStochasticFilter deviation="0.005"/>
			</GasPressureSensor>
			<GasPressureSensor input="HALO" moduleName="ppO2_HALO" gasType="O2">
				<alarms>
					<critical_low min="0" max="19"/>
					<warning_low min="19" max="20.665"/>
					<warning_high min="23.3314" max="24.6646"/>
					<critical_high min="24.6646" max="4000"/>
				</alarms>
				<normalStochasticFilter deviation="0.005"/>
			</GasPressureSensor>
    		<GasConcentrationSensor input="HALO" moduleName="Humidity_HALO" gasType="VAPOR">
				<alarms>
					<critical_low min="0" max="0.40"/>
					<warning_low min="0.40" max="0.50"/>
					<warning_high min="0.61" max="0.70"/>
					<critical_high min="0.70" max="1.00"/>
				</alarms>
				<normalStochasticFilter deviation="0.005"/>
			</GasConcentrationSensor>
			<TotalPressureSensor input="HALO" moduleName="Total_Cabin_Pressure_HALO">
				<alarms>
					<critical_low min="0" max="87.56342"/>
					<warning_low min="87.56342" max="100.31872"/>
					<warning_high min="102.7319" max="104.8003"/>
					<critical_high min="104.8003" max="110" />
				</alarms>
				<normalStochasticFilter deviation="0.005"/>
			</TotalPressureSensor>
		</environment>
	</Sensors>
</biosim>"""

# Malfunction intensities for combinations
MALFUNCTION_INTENSITIES = ['MEDIUM_MALF', 'SEVERE_MALF']

# Malfunction templates for different anomaly types with configurable intensity
MALFUNCTION_TEMPLATES = {
    'CO2 Scrubber Valve Leak': {
        'description': 'VCCR CO2 scrubber valve malfunction causing CO2 buildup',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'CO2_Store', 'ppCO2_IHab'],
        'default_intensity': 'SEVERE_MALF'
    },
    'Fan Bearing Wear': {
        'description': 'VCCR fan bearing degradation affecting air circulation',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'air circulation', 'ppCO2_IHab'],
        'default_intensity': 'MEDIUM_MALF'
    },
    'Absorption Bed Saturated': {
        'description': 'VCCR absorption bed saturation reducing CO2 removal efficiency',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'CO2_Store', 'ppCO2_IHab'],
        'default_intensity': 'SEVERE_MALF'
    },
    'Heater Coil Failure': {
        'description': 'VCCR heater coil malfunction affecting temperature control',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'temperature control', 'ppCO2_IHab'],
        'default_intensity': 'SEVERE_MALF'
    },
    "VCCR": {
        'description': 'VCCR system malfunction',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="0"/>',
        'affected_systems': ['VCCR'],
        'default_intensity': 'MEDIUM_MALF'
    },
    "Dehumidifier": {
        'description': 'Dehumidifier system malfunction',
        'component': 'Dehumidifier',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="0"/>',
        'affected_systems': ['Dehumidifier'],
        'default_intensity': 'SEVERE_MALF'
    },
    "OGS": {
        'description': 'Oxygen Generation System malfunction',
        'component': 'OGS',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['OGS', 'O2_Store'],
        'default_intensity': 'SEVERE_MALF'
    },
    "Water_Distiller": {
        'description': 'Water Recovery System malfunction',
        'component': 'WaterRS',
        'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['WaterRS', 'Potable_Water_Store'],
        'default_intensity': 'MEDIUM_MALF'
    }
}

# Default malfunction template for unknown anomalies
DEFAULT_MALFUNCTION = {
    'description': 'Generic VCCR malfunction',
    'component': 'VCCR',
    'malfunction_xml': '<malfunction intensity="{intensity}" length="PERMANENT_MALF" occursAtTick="10"/>',
    'affected_systems': ['VCCR', 'general systems'],
    'default_intensity': 'MEDIUM_MALF'
}

# Malfunction templates for different anomaly types
MALFUNCTION_TEMPLATES = {
    'CO2 Scrubber Valve Leak': {
        'description': 'VCCR CO2 scrubber valve malfunction causing CO2 buildup',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'CO2_Store', 'ppCO2_IHab']
    },
    'Fan Bearing Wear': {
        'description': 'VCCR fan bearing degradation affecting air circulation',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="MEDIUM_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'air circulation', 'ppCO2_IHab']
    },
    'Absorption Bed Saturated': {
        'description': 'VCCR absorption bed saturation reducing CO2 removal efficiency',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'CO2_Store', 'ppCO2_IHab']
    },
    'Heater Coil Failure': {
        'description': 'VCCR heater coil malfunction affecting temperature control',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR', 'temperature control', 'ppCO2_IHab']
    },
    "VCCR": {
        'description': 'VCCR system malfunction',
        'component': 'VCCR',
        'malfunction_xml': '<malfunction intensity="MEDIUM_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['VCCR']
    },
    "Dehumidifier": {
        'description': 'Dehumidifier system malfunction',
        'component': 'Dehumidifier',
        'malfunction_xml': '<malfunction intensity="SEVERE_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
        'affected_systems': ['Dehumidifier']
    },
    "Sim Environment": {
		'description': 'Sim Environment system malfunction',
		'component': 'SimEnvironment',
		'malfunction_xml': '<malfunction intensity="MEDIUM_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
		'affected_systems': ['SimEnvironment']
	},
}

# Default malfunction template for unknown anomalies
DEFAULT_MALFUNCTION = {
    'description': 'Generic VCCR malfunction',
    'component': 'VCCR',
    'malfunction_xml': '<malfunction intensity="MEDIUM_MALF" length="PERMANENT_MALF" occursAtTick="10"/>',
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
    print(f"[PHYS_DIAG] Looking up malfunction config for anomaly: '{anomaly_name}'")
    if anomaly_name in MALFUNCTION_TEMPLATES:
        print(f"[PHYS_DIAG] Found exact match for anomaly: '{anomaly_name}'")
        return MALFUNCTION_TEMPLATES[anomaly_name]
    
    # Try partial matches
    for key, config in MALFUNCTION_TEMPLATES.items():
        if key.lower() in anomaly_name.lower() or anomaly_name.lower() in key.lower():
            return config
    
    # Return default if no match found
    return DEFAULT_MALFUNCTION

def inject_malfunction_into_component(template: str, component_name: str, malfunction_xml: str) -> str:
    """
    Inject malfunction XML into the specified component in the BioSim template.
    
    Args:
        template: Base BioSim XML template
        component_name: Name of the component to add malfunction to (e.g., 'VCCR', 'Dehumidifier')
        malfunction_xml: Malfunction XML string to inject
        
    Returns:
        Modified template with malfunction injected
    """
    import re
    
    print(f"[BIOSIM_TEMPLATE] Injecting malfunction into component: {component_name}")
    
    # Generic pattern to find any component by name and inject malfunction before its closing tag
    pattern = rf'(<{component_name}[^>]*>.*?)(></{component_name}>|</{component_name}>)'
    replacement = r'\1\n\t\t\t\t' + malfunction_xml + r'\n\t\t\t\2'
    
    # Apply the replacement
    modified_template = re.sub(pattern, replacement, template, flags=re.DOTALL)
    
    # Check if injection was successful
    if malfunction_xml in modified_template:
        print(f"[BIOSIM_TEMPLATE] Successfully injected malfunction into {component_name}")
    else:
        print(f"[BIOSIM_TEMPLATE] WARNING: Failed to inject malfunction into {component_name}")
        
        # Debug: Show what component sections were found
        debug_pattern = rf'<{component_name}[^>]*>.*?</{component_name}>'
        debug_match = re.search(debug_pattern, template, flags=re.DOTALL)
        if debug_match:
            print(f"[BIOSIM_TEMPLATE] Found {component_name} section: {debug_match.group()[:200]}...")
        else:
            print(f"[BIOSIM_TEMPLATE] No {component_name} section found in template")
    
    return modified_template

def generate_config(anomaly_name: Union[str, List[str]], duration_seconds: int, intensities: List[str] = None) -> str:
    """
    Generate complete BioSim configuration for one or more anomalies.
    
    Args:
        anomaly_name: Single anomaly name (str) or list of anomaly names for combinations
        duration_seconds: Duration of the simulation in seconds
        intensities: List of intensities for each anomaly (only used for multi-anomaly)
        
    Returns:
        Complete XML configuration string
    """
    config_content = BASE_BIOSIM_TEMPLATE.format(max_ticks=int(duration_seconds))
    
    # Handle single anomaly case (backwards compatibility)
    if isinstance(anomaly_name, str):
        malfunction_config = get_malfunction_config(anomaly_name)
        
        # Use default intensity from template
        intensity = malfunction_config.get('default_intensity', 'MEDIUM_MALF')
        
        # Format the malfunction XML with the intensity
        formatted_malfunction_xml = malfunction_config['malfunction_xml'].format(intensity=intensity)
        
        # Inject the malfunction into the appropriate component
        config_content = inject_malfunction_into_component(
            template=config_content,
            component_name=malfunction_config['component'],
            malfunction_xml=formatted_malfunction_xml
        )
        
        print(f"[BIOSIM_TEMPLATE] Generated config with {intensity} malfunction in {malfunction_config['component']}")
        return config_content
    
    # Handle multiple anomalies case
    if isinstance(anomaly_name, list):
        print(f"[BIOSIM_TEMPLATE] Generating multi-anomaly config for: {anomaly_name}")
        
        # Process each anomaly in the combination
        for i, single_anomaly in enumerate(anomaly_name):
            try:
                # Get malfunction config for this anomaly
                malfunction_config = get_malfunction_config(single_anomaly)
                
                # Use provided intensity or default from template
                if intensities and i < len(intensities):
                    intensity = intensities[i]
                else:
                    intensity = malfunction_config.get('default_intensity', 'MEDIUM_MALF')
                
                # Format the malfunction XML with the intensity
                formatted_malfunction_xml = malfunction_config['malfunction_xml'].format(intensity=intensity)
                
                # Inject the malfunction into the appropriate component
                config_content = inject_malfunction_into_component(
                    template=config_content,
                    component_name=malfunction_config['component'],
                    malfunction_xml=formatted_malfunction_xml
                )
                
                print(f"[BIOSIM_TEMPLATE] Injected {intensity} malfunction for {single_anomaly} into {malfunction_config['component']}")
                
            except Exception as e:
                print(f"[BIOSIM_TEMPLATE] ❌ Failed to inject malfunction for {single_anomaly}: {e}")
        
        print(f"[BIOSIM_TEMPLATE] Generated multi-anomaly config with {len(anomaly_name)} malfunctions")
        return config_content
    
    # Fallback case
    print(f"[BIOSIM_TEMPLATE] ⚠️ Invalid anomaly_name type: {type(anomaly_name)}")
    return config_content
