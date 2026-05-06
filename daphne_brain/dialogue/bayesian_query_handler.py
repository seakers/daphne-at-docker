import json
import os
from AT.diagnosis.bayesian.ECLSS_Bayesian_Network_Learned import get_probabilities
from AT.diagnosis.bayesian.reduce_entropy import calculate_entropy, select_best_evidence
import re

class BayesianQueryHandler:
    """
    Handle queries related to the Bayesian network and probability calculations
    """
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # Get the root directory (daphne_brain app root)
        self.app_root = os.path.dirname(self.current_dir)
        
        # Load probability dictionaries using paths relative to app root
        self.split_probability_dict_path = os.path.join(
            self.app_root, "AT/diagnosis/bayesian/split_probability_dict.json")
        self.hidden_probabilities_dict_path = os.path.join(
            self.app_root, "AT/diagnosis/bayesian/hidden_probabilities_dict.json")
        
        with open(self.split_probability_dict_path, "r") as file:
            self.split_probability_dict = json.load(file)
        with open(self.hidden_probabilities_dict_path, "r") as file:
            self.hidden_probabilities_dict = json.load(file)
            
        self.measurement_nodes = [
            "high ppO2_IHab (IHab)", "low ppO2_IHab (IHab)",
            "high ppO2_IHab (IHab) (t-1)", "low ppO2_IHab (IHab) (t-1)",
            "high ppO2_HALO (HALO)", "low ppO2_HALO (HALO)",
            "high ppO2_HALO (HALO) (t-1)", "low ppO2_HALO (HALO) (t-1)",
            "high ppCO2_IHab (IHab)", "low ppCO2_IHab (IHab)",
            "high ppCO2_IHab (IHab) (t-1)", "low ppCO2_IHab (IHab) (t-1)",
            "high ppCO2_HALO (HALO)", "low ppCO2_HALO (HALO)",
            "high ppCO2_HALO (HALO) (t-1)", "low ppCO2_HALO (HALO) (t-1)",
            "high Humidity_IHab (IHab)", "low Humidity_IHab (IHab)",
            "high Humidity_IHab (IHab) (t-1)", "low Humidity_IHab (IHab) (t-1)",
            "high Humidity_HALO (HALO)", "low Humidity_HALO (HALO)",
            "high Humidity_HALO (HALO) (t-1)", "low Humidity_HALO (HALO) (t-1)",
            "high Total_Cabin_Pressure_IHab (IHab)", "low Total_Cabin_Pressure_IHab (IHab)",
            "high Total_Cabin_Pressure_IHab (IHab) (t-1)", "low Total_Cabin_Pressure_IHab (IHab) (t-1)",
            "high Total_Cabin_Pressure_HALO (HALO)", "low Total_Cabin_Pressure_HALO (HALO)",
            "high Total_Cabin_Pressure_HALO (HALO) (t-1)", "low Total_Cabin_Pressure_HALO (HALO) (t-1)"
        ]
    
    def get_hidden_components(self):
        """Return a list of all hidden components in the model"""
        return list(self.hidden_probabilities_dict.keys())
    
    def explain_model_structure(self):
        """Explain the structure of the Bayesian network"""
        # Create a high-level description
        explanation = {
            "voice_message": "The Bayesian network models anomalies and their related measurements and components.",
            "visual_message_type": ["text"],
            "visual_message": [
                "The Bayesian network has three main types of nodes:",
                "1. Anomaly nodes: Represent system anomalies (failures)",
                "2. Measurement nodes: Represent observable telemetry values",
                "3. Hidden component nodes: Represent components that can be inspected, but aren't automatically measured"
            ],
            "writer": "daphne"
        }
        return explanation
    
    def explain_probability_calculation(self):
        """Explain how anomaly probabilities are calculated"""
        explanation = {
            "voice_message": "Anomaly probabilities are calculated using Bayesian inference from observed evidence.",
            "visual_message_type": ["text"],
            "visual_message": [
                "Probabilities are calculated in these steps:",
                "1. Each anomaly has a prior probability (baseline chance of occurrence)",
                "2. Telemetry measurements provide evidence through conditional probability tables",
                "3. For each measurement outside normal ranges, the model updates probabilities",
                "4. Additional evidence from component inspections further updates probabilities",
                "5. A Variable Elimination algorithm calculates the posterior probabilities",
                "6. Results are normalized to sum to 1.0"
            ],
            "writer": "daphne"
        }
        return explanation
        
    def what_if_evidence(self, current_telemetry, current_evidence, hypothetical_context):
        """
        Calculate how probabilities would change if we add evidence about components and measurements
        """
        # Get current probabilities without the new evidence
        current_probs, _, _ = get_probabilities(current_telemetry, current_evidence)
        
        # Create evidence dictionary with the new component evidence
        additional_evidence = current_evidence.copy()
        if "components" in hypothetical_context:
            for component, state in hypothetical_context["components"].items():
                additional_evidence[component] = state

        # The llm is return low/high + measurement name, so to find that in measurement ranges, stripping it of low/high
        from AT.diagnosis.bayesian.reduced_ranges import measurement_ranges
        
        updated_telemetry = current_telemetry.copy()
        print("hypothetical context", hypothetical_context)
        if "measurements" in hypothetical_context:
            for parameter, state_value in hypothetical_context["measurements"].items():
                state_value = int(state_value)
                
                # Determine low/high and strip prefix
                direction = None
                base_param = parameter
                if parameter.startswith("high "):
                    direction = "high"
                    base_param = parameter[len("high "):]
                elif parameter.startswith("low "):
                    direction = "low"
                    base_param = parameter[len("low "):]
                
                # Strip (t-1) suffix to lookup in measurement_ranges 
                lookup_param = base_param.replace(" (t-1)", "")
                
                # Map direction + state to threshold name
                if state_value == 0:
                    threshold_name = "Nominal"
                elif direction == "high" and state_value == 1:
                    threshold_name = "Exceeds_UpperCautionLimit"
                elif direction == "high" and state_value == 2:
                    threshold_name = "Exceeds_UpperWarningLimit"
                elif direction == "low" and state_value == 1:
                    threshold_name = "Exceeds_LowerCautionLimit"
                elif direction == "low" and state_value == 2:
                    threshold_name = "Exceeds_LowerWarningLimit"
                else:
                    print(f"Unknown direction/state: {direction}/{state_value}")
                    continue

                print("look up param", lookup_param)
                
                if lookup_param not in measurement_ranges:
                    print(f"Parameter {lookup_param} not found in measurement_ranges")
                    continue
                print("look up param in measurement ranges")
                bounds = measurement_ranges[lookup_param].get(threshold_name)
                if bounds:
                    low, high, _, _ = bounds
                    if low is not None and high is not None:
                        val = (low + high) / 2.0
                    elif low is not None:
                        val = low + (low * 0.1) if low != 0 else 1.0
                    elif high is not None:
                        val = high - (abs(high) * 0.1) if high != 0 else -1.0
                    else:
                        val = 0.0
                    print("final vallll", val)
                    
                    # Set both current and t-1 telemetry to the same value
                    updated_telemetry[lookup_param] = val
                    updated_telemetry[f"{lookup_param} (t-1)"] = val
                    print(f"Telemetry override: {lookup_param} = {val} (threshold: {threshold_name})")

        # Calculate new probabilities with the added evidence (includes best_evidence)
        new_probs, best_evidence, _ = get_probabilities(updated_telemetry, additional_evidence)
        
        top_5_probabilities = dict(sorted(new_probs.items(), 
                                     key=lambda item: item[1], 
                                     reverse=True)[:5])
        
        # Create response
        evidence_list = []
        if "components" in hypothetical_context:
            for component, state in hypothetical_context["components"].items():
                state_str = "damaged" if state == 4 else "normal"
                evidence_list.append(f"{component} is {state_str}")
                
        if "measurements" in hypothetical_context:
            for param, state in hypothetical_context["measurements"].items():
                evidence_list.append(f"{param} is {state}")

        evidence_display = ", ".join(evidence_list) if evidence_list else "None"

        formatted_probabilities = "\n".join([f"{anomaly}: {prob:.4f}" for anomaly, prob in top_5_probabilities.items()])
        visual_message = [f"If this hypothetical evidence is added: {evidence_display}\n\nThe new probabilities would be:\n{formatted_probabilities}"]

        print("best evidenceee in hypothetical", best_evidence)
        
        return {
            "voice_message": f"Adding the evidence would change anomaly probabilities.",
            "visual_message_type": ["text"],
            "visual_message": visual_message,
            "writer": "daphne",
            "options": ["Add to Diagnosis History"],
            "optionsCallbackEvent": "addHypotheticalDiagnosis",
            "hypothetical_context": hypothetical_context,
            "hypothetical_data": {
                "probabilities": new_probs,
                "additional_evidence": additional_evidence,
                "best_evidence": best_evidence,
                "current_telemetry_values": updated_telemetry,
                "diagnosis_list": [{
                    "anomaly": anomaly,
                    "probability": prob
                } for anomaly, prob in top_5_probabilities.items()]
            }
        }
    
    def best_evidence_to_collect(self, current_telemetry, current_evidence):
        """
        Determine which evidence would be most informative to collect next
        """
        _, best_evidence, hidden_components = get_probabilities(current_telemetry, current_evidence)
        
        if not best_evidence:
            return {
                "voice_message": "No additional evidence would significantly improve diagnostic confidence.",
                "visual_message_type": ["text"],
                "visual_message": ["No additional evidence would significantly improve diagnostic confidence with the current telemetry values."],
                "writer": "daphne"
            }
        
        associated_anomalies = []
        for anomaly, data in self.hidden_probabilities_dict.get(best_evidence, {}).items():
            associated_anomalies.append(anomaly)
        
        return {
            "voice_message": f"Collecting evidence about {best_evidence} would be most informative.",
            "visual_message_type": ["text"],
            "visual_message": [
                f"The most informative evidence to collect next is: {best_evidence}",
                f"This component is associated with anomalies: {', '.join(associated_anomalies)}",
                "Checking this component would reduce uncertainty the most in the current diagnosis."
            ],
            "writer": "daphne"
        }
    
    def explain_evidence_impact(self, anomaly):
        """
        Explain which evidence has the most impact on a specific anomaly
        """
        relevant_components = []
        for component, anomalies in self.hidden_probabilities_dict.items():
            if anomaly in anomalies:
                relevant_components.append(component)
        
        relevant_measurements = []
        for measurement, anomalies in self.split_probability_dict.items():
            if anomaly in anomalies:
                relevant_measurements.append(measurement)
        
        return {
            "voice_message": f"Several pieces of evidence affect the probability of {anomaly}.",
            "visual_message_type": ["text"],
            "visual_message": [
                f"Evidence that affects {anomaly} probability:",
                f"Hidden components: {', '.join(relevant_components[:5])}{'...' if len(relevant_components) > 5 else ''}",
                f"Measurements: {', '.join(relevant_measurements[:5])}{'...' if len(relevant_measurements) > 5 else ''}"
            ],
            "writer": "daphne"
        }
    
    def handle_query(self, query, current_telemetry, current_evidence=None, hypothetical_context=None):
        """
        Main method to handle various Bayesian queries using LLM for intent classification
        """
        if hypothetical_context is None:
            hypothetical_context = {"components": {}, "measurements": {}}
            
        intent = self.classify_query_intent(query)
        print("intent for bayesian query", intent)
        
        if intent == "probability_calculation_explanation":
            res = self.explain_probability_calculation()
            res["hypothetical_context"] = hypothetical_context
            return res
            
        elif intent == "model_structure_explanation":
            res = self.explain_model_structure()
            res["hypothetical_context"] = hypothetical_context
            return res
            
        elif intent == "what_if_evidence":
            extracted_data = self.extract_hypothetical_evidence(query)
            
            if extracted_data.get("needs_clarification"):
                return {
                    "voice_message": "I need some clarification.",
                    "visual_message_type": ["text"],
                    "visual_message": [extracted_data["needs_clarification"]],
                    "writer": "daphne",
                    "hypothetical_context": hypothetical_context
                }
            
            if extracted_data.get("is_continuation"):
                if "components" not in hypothetical_context:
                    hypothetical_context["components"] = {}
                if "measurements" not in hypothetical_context:
                    hypothetical_context["measurements"] = {}
                hypothetical_context["components"].update(extracted_data.get("components", {}))
                hypothetical_context["measurements"].update(extracted_data.get("measurements", {}))
            else:
                hypothetical_context["components"] = extracted_data.get("components", {})
                hypothetical_context["measurements"] = extracted_data.get("measurements", {})
            
            if hypothetical_context["components"] or hypothetical_context["measurements"]:
                return self.what_if_evidence(current_telemetry, current_evidence, hypothetical_context)
            else:
                return {
                    "voice_message": "I need to know which component or measurement you're asking about.",
                    "visual_message_type": ["text"],
                    "visual_message": [
                        "To answer 'what if' queries, I need to know which component or measurement you're asking about.",
                        "For example: 'What if CDRA Failure Component showed damage?' or 'What if ppO2 IHab is nominal?'"
                    ],
                    "writer": "daphne",
                    "hypothetical_context": hypothetical_context
                }
                
        elif intent == "best_evidence":
            res = self.best_evidence_to_collect(current_telemetry, current_evidence)
            res["hypothetical_context"] = hypothetical_context
            return res
            
        elif intent == "evidence_impact":
            anomaly = self.extract_anomaly(query)
            
            if anomaly:
                res = self.explain_evidence_impact(anomaly)
            else:
                res = {
                    "voice_message": "I need to know which anomaly you're asking about.",
                    "visual_message_type": ["text"],
                    "visual_message": [
                        "To explain evidence impact, I need to know which anomaly you're interested in.",
                        "For example: 'What evidence affects CDRA Failure probability?'"
                    ],
                    "writer": "daphne"
                }
                
        else:
            # Default response for unrecognized Bayesian queries
            return {
                "voice_message": "I can answer questions about the Bayesian diagnosis model.",
                "visual_message_type": ["text"],
                "visual_message": [
                    "I can answer questions about the Bayesian diagnosis model, such as:",
                    "- How are the anomaly probabilities calculated?",
                    "- What would happen if we add evidence that a component is damaged?",
                    "- What's the most informative evidence to collect next?",
                    "- Which evidence has the biggest impact on a specific anomaly?"
                ],
                "writer": "daphne"
            }

    def classify_query_intent(self, query):
        """
        Use LLM to classify the intent of a Bayesian network query
        
        Args:
            query: The user's query text
            
        Returns:
            Classified intent string
        """
        from openai import OpenAI
        import os
        
        # Initialize the OpenAI client with API key from environment
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        print("query for bayesian query", query)
        
        # Prepare the prompt for intent classification
        prompt = f"""
        Classify the following user query about a Bayesian network diagnostic system into one of these categories:
        - probability_calculation_explanation: Questions about how probabilities are calculated
        - model_structure_explanation: Questions about the structure of the Bayesian network
        - what_if_evidence: Questions about hypothetical scenarios like:
            * "what if CDRA component is damaged"
            * "what if ppO2 is nominal"
            * "what if humidity is in warning and excess CO2 component is active"
            * "also add ppCO2 as very high" (continuation of previous scenario)
        - best_evidence: Questions about what evidence would be most informative to collect
        - evidence_impact: Questions about which evidence impacts specific anomalies

        Only classify the query into one of these categories. Return only one word in probability_calculation_explanation, model_structure_explanation, what_if_evidence, best_evidence, evidence_impact.
        
        Query: {query}
        
        Return only the category name without explanation.
        """
        
        try:
            # Call the LLM API for classification
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,  # Low temperature for consistent responses
                max_tokens=20     # We only need a short response
            )
            
            # Extract and return the classified intent
            intent = response.choices[0].message.content.strip().lower()

            print("intent for bayesian query", intent)

            return intent
            
        except Exception as e:
            print(f"Error in LLM classification: {e}")
            # Default to 'other' in case of errors
            return 'other'

    def extract_hypothetical_evidence(self, query):
        """
        Use LLM to extract component names and measurement overrides from a query
        """
        from openai import OpenAI
        import os
        
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        valid_components = list(self.hidden_probabilities_dict.keys())
        valid_measurements = self.measurement_nodes
        
        prompt = f"""
        Extract the component names and measurement overrides from the following query about a Bayesian network.
        The query is asking what would happen if components or measurements had certain evidence.

        Valid components include: {', '.join(valid_components)}
        Valid measurements include: {', '.join(valid_measurements)}

        Query: {query}

        If the user's query is ambiguous about measurements (e.g., "ppO2 is low" without specifying IHab or HALO, or without specifying if it's the current reading or previous reading t-1), set "needs_clarification" to a string asking them to clarify. Example: "Which module are you referring to — IHab or HALO? And should this apply to the current reading, the previous reading (t-1), or both?". If they say "current ppO2 IHab is low", that is not ambiguous.

        For component states:
        - Map to "true" if user says: damaged, positive, present, abnormal, fault, failure, or values 3, 4, 5
        - Map to "false" if user says: undamaged, negative, absent, normal, intact, working, operational, or values 1, 2

        For measurement states:
        - Map to 0 if user says: nominal, normal
        - Map to 1 if user says: caution, slightly high/low
        - Map to 2 if user says: critical, warning, very high/low

        Note for measurements: "low ppO2" refers to the "low ppO2_..." nodes, while "high ppO2" refers to "high ppO2_..." nodes. If a user says "nominal", it means both high and low nodes are 0.

        Also determine if this is a continuation of a previous scenario ("also add...", "what about if...") or a new scenario. Set "is_continuation" to true or false.

        Output MUST be valid JSON only:
        {{
          "components": {{"[HIDDEN] CDRA Failure Component": "true"}},
          "measurements": {{"high ppCO2_IHab (IHab)": 2}},
          "needs_clarification": null,
          "is_continuation": false
        }}
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=250
            )
            
            result_text = response.choices[0].message.content.strip()
            result_text = re.sub(r'```(?:json)?\s*', '', result_text)
            result_text = re.sub(r'\s*```', '', result_text)
            print("extracted hypothetical evidence:", result_text)
            
            json_data = json.loads(result_text)
            
            # process components
            components = {}
            for key, value in json_data.get("components", {}).items():
                if key in valid_components:
                    components[key] = 4 if str(value).lower() == "true" else 1
            json_data["components"] = components
            
            # measurements don't need translation, they are already 0, 1, 2
            measurements = {}
            for key, value in json_data.get("measurements", {}).items():
                if key in valid_measurements:
                    measurements[key] = value
            json_data["measurements"] = measurements
            
            return json_data
            
        except Exception as e:
            print(f"Error in LLM entity extraction: {e}")
            return {"components": {}, "measurements": {}, "needs_clarification": None, "is_continuation": False}

    def extract_anomaly(self, query):
        """
        Use LLM to extract anomaly name from a query
        
        Args:
            query: The user's query text
            
        Returns:
            Extracted anomaly name or None if not found
        """
        from openai import OpenAI
        import os
        
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Collect all anomalies from the probability dictionaries
        all_anomalies = set()
        for anomalies in self.split_probability_dict.values():
            all_anomalies.update(anomalies.keys())
        
        # Convert to list for the prompt
        anomaly_list = list(all_anomalies)[:20]  # Limit to 20 for reasonable prompt size
        
        # Prepare the prompt for entity extraction
        prompt = f"""
        Extract the anomaly name from the following query about evidence impact in a Bayesian network.
        The query is asking which evidence affects a particular anomaly's probability.
        
        Valid anomalies include: {', '.join(anomaly_list)}
        
        Query: {query}
        
        Output format:
        Anomaly: [exact anomaly name from the list or NONE if not found]
        """
        
        try:
            # Call the LLM API for entity extraction
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,  # Low temperature for consistent responses
                max_tokens=50     # Limit response length
            )
            
            # Extract the information from the response
            result_text = response.choices[0].message.content.strip()
            
            # Parse the result
            anomaly = None
            
            for line in result_text.split('\n'):
                if line.lower().startswith('anomaly:'):
                    anomaly = line[len('anomaly:'):].strip()
                    if anomaly.upper() == 'NONE':
                        anomaly = None
                    break
            
            return anomaly
            
        except Exception as e:
            print(f"Error in LLM entity extraction: {e}")
            return None