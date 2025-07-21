#!/usr/bin/env python3
"""
TEC: World Anvil Map Tools - Automated Mapping System
Automate worldbuilding maps on World Anvil with interactive markers and dynamic layers
Protocol: TEC_CSS_072125_V1 - Map Automation Extensions
"""

import requests
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorldAnvilMapAPI:
    """
    World Anvil Maps API integration for automated map management
    Extends the base World Anvil API with mapping-specific functionality
    """
    
    def __init__(self, app_key: Optional[str] = None, auth_token: Optional[str] = None, world_id: Optional[str] = None):
        self.base_url = "https://www.worldanvil.com/api/boromir"
        self.app_key = app_key or os.getenv('WORLD_ANVIL_APP_KEY')
        self.auth_token = auth_token or os.getenv('WORLD_ANVIL_AUTH_TOKEN')
        self.world_id = world_id or os.getenv('WORLD_ANVIL_WORLD_ID')
        
        if not all([self.app_key, self.auth_token, self.world_id]):
            logger.warning("Missing World Anvil credentials for map operations")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            'x-application-key': self.app_key or '',
            'x-auth-token': self.auth_token or '',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def add_marker_to_map(self, map_id: str, article_id: str, x_coord: float, y_coord: float, 
                         label: Optional[str] = None, icon_type: str = 'default') -> Dict[str, Any]:
        """
        Add a marker to a World Anvil map that links to an article
        
        Args:
            map_id: The ID of the map to add the marker to
            article_id: The ID of the article the marker should link to
            x_coord: X coordinate for marker placement (0-100 percentage)
            y_coord: Y coordinate for marker placement (0-100 percentage)
            label: Optional label for the marker
            icon_type: Type of icon to use for the marker
            
        Returns:
            API response data
        """
        
        # Validate coordinates
        if not (0 <= x_coord <= 100) or not (0 <= y_coord <= 100):
            return {
                'success': False,
                'error': 'Coordinates must be between 0 and 100 (percentage)',
                'message': 'Invalid coordinates provided'
            }
        
        payload = {
            'map_id': map_id,
            'article_id': article_id,
            'x_position': x_coord,
            'y_position': y_coord,
            'icon_type': icon_type
        }
        
        if label:
            payload['label'] = label
        
        return self._make_request('PUT', f'/maps/{map_id}/markers', payload)
    
    def create_map_layer(self, map_id: str, layer_name: str, layer_type: str = 'custom', 
                        is_visible: bool = True) -> Dict[str, Any]:
        """
        Create a new layer on a World Anvil map
        
        Args:
            map_id: The ID of the map to add the layer to
            layer_name: Name of the new layer
            layer_type: Type of layer (security, corporate, mystical, historical, custom)
            is_visible: Whether the layer should be visible by default
            
        Returns:
            API response data
        """
        
        payload = {
            'name': layer_name,
            'type': layer_type,
            'visible': is_visible,
            'world': self.world_id
        }
        
        return self._make_request('POST', f'/maps/{map_id}/layers', payload)
    
    def update_map_layer_visibility(self, map_id: str, layer_id: str, is_visible: bool) -> Dict[str, Any]:
        """
        Toggle the visibility of a map layer
        
        Args:
            map_id: The ID of the map
            layer_id: The ID of the layer to toggle
            is_visible: Whether to show or hide the layer
            
        Returns:
            API response data
        """
        
        payload = {
            'visible': is_visible
        }
        
        return self._make_request('PATCH', f'/maps/{map_id}/layers/{layer_id}', payload)
    
    def get_map_info(self, map_id: str) -> Dict[str, Any]:
        """
        Get information about a specific map
        
        Args:
            map_id: The ID of the map to retrieve
            
        Returns:
            Map information including layers and markers
        """
        
        return self._make_request('GET', f'/maps/{map_id}')
    
    def list_world_maps(self) -> Dict[str, Any]:
        """
        List all maps in the current world
        
        Returns:
            List of maps in the world
        """
        
        return self._make_request('GET', f'/worlds/{self.world_id}/maps')
    
    def _make_request(self, method: str, endpoint: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to World Anvil Maps API"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=payload)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=payload)
            elif method == 'PATCH':
                response = requests.patch(url, headers=headers, json=payload)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            logger.info(f"World Anvil Maps API {method} {endpoint} - Status: {response.status_code}")
            
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
                'message': 'Request successful'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"World Anvil Maps API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Request failed'
            }


class TECAstrodigitalMapper:
    """
    TEC-specific mapping tools for the Astradigital Ocean
    Implements automated map management for TEC universe
    """
    
    def __init__(self, map_api: WorldAnvilMapAPI):
        self.api = map_api
        
        # TEC-specific map layer types
        self.tec_layers = {
            'security': 'Eldoran Military & Firewalls',
            'corporate': 'Eldora Studios & Data Centers', 
            'mystical': 'Reaper\'s Gold & Manifestations',
            'historical': 'Corporate Wars Timeline'
        }
        
        # TEC-specific marker types
        self.tec_markers = {
            'headquarters': 'Corporate HQ',
            'data_node': 'Network Node',
            'character_location': 'Character Position',
            'corrupted_zone': 'Data Corruption',
            'manifestation': 'Astral Manifestation',
            'military_base': 'Security Installation'
        }
    
    def setup_astradigital_ocean_map(self, map_id: str) -> Dict[str, Any]:
        """
        Set up the complete Astradigital Ocean map with all TEC layers
        
        Args:
            map_id: The ID of the Astradigital Ocean base map
            
        Returns:
            Setup results for all layers
        """
        
        results = []
        
        # Create each TEC layer
        for layer_type, layer_name in self.tec_layers.items():
            result = self.api.create_map_layer(
                map_id=map_id,
                layer_name=layer_name,
                layer_type=layer_type,
                is_visible=(layer_type == 'corporate')  # Start with corporate layer visible
            )
            results.append({
                'layer': layer_type,
                'name': layer_name,
                'result': result
            })
        
        return {
            'map_id': map_id,
            'layers_created': len(results),
            'results': results,
            'setup_complete': all(r['result'].get('success', False) for r in results)
        }
    
    def add_eldora_studios_hq(self, map_id: str, article_id: str, 
                             x_coord: float = 50.0, y_coord: float = 30.0) -> Dict[str, Any]:
        """
        Add Eldora Studios HQ marker to the map
        
        Args:
            map_id: The Astradigital Ocean map ID
            article_id: Article ID for Eldora Studios organization
            x_coord: X coordinate (default: center-left)
            y_coord: Y coordinate (default: upper area)
            
        Returns:
            Marker creation result
        """
        
        return self.api.add_marker_to_map(
            map_id=map_id,
            article_id=article_id,
            x_coord=x_coord,
            y_coord=y_coord,
            label="Eldora Studios HQ",
            icon_type="headquarters"
        )
    
    def add_character_location(self, map_id: str, character_name: str, 
                              article_id: str, x_coord: float, y_coord: float) -> Dict[str, Any]:
        """
        Add a character location marker to the map
        
        Args:
            map_id: The map ID
            character_name: Name of the character
            article_id: Character article ID
            x_coord: X coordinate
            y_coord: Y coordinate
            
        Returns:
            Marker creation result
        """
        
        return self.api.add_marker_to_map(
            map_id=map_id,
            article_id=article_id,
            x_coord=x_coord,
            y_coord=y_coord,
            label=f"{character_name}'s Location",
            icon_type="character_location"
        )
    
    def add_data_corruption_zone(self, map_id: str, zone_name: str, 
                                article_id: str, x_coord: float, y_coord: float) -> Dict[str, Any]:
        """
        Add a data corruption zone marker
        
        Args:
            map_id: The map ID
            zone_name: Name of the corrupted zone
            article_id: Plot article ID describing the corruption
            x_coord: X coordinate
            y_coord: Y coordinate
            
        Returns:
            Marker creation result
        """
        
        return self.api.add_marker_to_map(
            map_id=map_id,
            article_id=article_id,
            x_coord=x_coord,
            y_coord=y_coord,
            label=f"Corrupted Zone: {zone_name}",
            icon_type="corrupted_zone"
        )
    
    def create_historical_timeline_layers(self, map_id: str, 
                                        timeline_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple historical layers for timeline visualization
        
        Args:
            map_id: The map ID
            timeline_events: List of events with 'name', 'year', and 'description'
            
        Returns:
            List of layer creation results
        """
        
        results = []
        
        for event in timeline_events:
            layer_name = f"{event['year']}: {event['name']}"
            result = self.api.create_map_layer(
                map_id=map_id,
                layer_name=layer_name,
                layer_type='historical',
                is_visible=False  # Historical layers start hidden
            )
            results.append({
                'event': event,
                'layer_name': layer_name,
                'result': result
            })
        
        return results


# CLI Interface and Examples
if __name__ == "__main__":
    print("🗺️  TEC World Anvil Map Tools")
    print("🎯 Automate the Astradigital Ocean mapping")
    print("=" * 50)
    
    # Initialize map API
    map_api = WorldAnvilMapAPI(
        app_key="YOUR_WORLD_ANVIL_APP_KEY",
        auth_token="YOUR_WORLD_ANVIL_AUTH_TOKEN",
        world_id="YOUR_WORLD_ANVIL_WORLD_ID"
    )
    
    # Initialize TEC mapper
    tec_mapper = TECAstrodigitalMapper(map_api)
    
    print("\n🚀 Example Operations:")
    
    # Example 1: Add Eldora Studios HQ marker
    print("\n1. Adding Eldora Studios HQ marker...")
    # Uncomment to test with real API:
    # result = tec_mapper.add_eldora_studios_hq(
    #     map_id="your_astradigital_ocean_map_id",
    #     article_id="your_eldora_studios_article_id",
    #     x_coord=45.0,  # Center-left position
    #     y_coord=25.0   # Upper area
    # )
    # print(f"Result: {result}")
    
    print("✅ Demo: Marker would be placed at coordinates (45, 25)")
    print("🔗 Links to: Eldora Studios Organization article")
    
    # Example 2: Set up complete Astradigital Ocean
    print("\n2. Setting up Astradigital Ocean layers...")
    # Uncomment to test with real API:
    # setup_result = tec_mapper.setup_astradigital_ocean_map("your_map_id")
    # print(f"Setup result: {setup_result}")
    
    print("✅ Demo: Would create 4 layers:")
    for layer_type, layer_name in tec_mapper.tec_layers.items():
        print(f"   • {layer_name} ({layer_type})")
    
    # Example 3: Add character locations
    print("\n3. Adding character location markers...")
    characters = [
        ("Polkin Rishall", "polkin_article_id", 60.0, 40.0),
        ("Airth", "airth_article_id", 30.0, 70.0),
        ("Mynx", "mynx_article_id", 80.0, 50.0),
        ("Kaelen", "kaelen_article_id", 40.0, 60.0)
    ]
    
    for name, article_id, x, y in characters:
        print(f"   • {name} at coordinates ({x}, {y})")
        # Uncomment to test with real API:
        # result = tec_mapper.add_character_location("map_id", name, article_id, x, y)
    
    # Example 4: Historical timeline
    print("\n4. Creating historical timeline layers...")
    timeline_events = [
        {"name": "Corporate Wars Begin", "year": "2157", "description": "The start of territorial conflicts"},
        {"name": "Eldora Studios Founded", "year": "2162", "description": "Digital revolution begins"},
        {"name": "First Manifestation", "year": "2165", "description": "Astral plane breach detected"},
        {"name": "Current Era", "year": "2170", "description": "Present day TEC universe"}
    ]
    
    for event in timeline_events:
        print(f"   • {event['year']}: {event['name']}")
        # Uncomment to test with real API:
        # layer_result = tec_mapper.create_historical_timeline_layers("map_id", [event])
    
    print("\n🎯 Map Automation Complete!")
    print("\n📋 To use with real World Anvil:")
    print("1. Set your API credentials in environment variables")
    print("2. Get your map ID from World Anvil")
    print("3. Get article IDs for your content")
    print("4. Uncomment the API calls above")
    print("5. Run the script to populate your maps!")
    
    print("\n🗺️  TEC Astradigital Ocean Features:")
    print("• Interactive markers linking to articles")
    print("• Layered view system (security, corporate, mystical, historical)")
    print("• Character location tracking")
    print("• Historical timeline visualization")
    print("• Automated corruption zone mapping")
    
    print("\n✨ Your digital universe now has navigation!")
