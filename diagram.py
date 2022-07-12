"""
Diagram as code  – VPN TGW attachment
"""
from diagrams import Diagram, Edge
from diagrams.aws.network import (
    TransitGateway,
    VPC,
    VPCCustomerGateway,
    SiteToSiteVpn,
    VPCCustomerGateway,
)

with Diagram("VPN TGW Attachment", show=False):
    tgw = TransitGateway("TGW")
    tgw - SiteToSiteVpn("Site-to-Site VPN") - VPCCustomerGateway("Primary PoP")
    tgw - SiteToSiteVpn("Site-to-Site VPN") - VPCCustomerGateway("Failover PoP")
