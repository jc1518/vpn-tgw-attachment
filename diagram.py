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
    RouteTable,
)
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.integration import Eventbridge

with Diagram("VPN Failover via TGW Attachment", show=False):
    tgw = TransitGateway("TGW")
    (
        tgw
        - Edge(label="primary vpn tgw attachment")
        - SiteToSiteVpn("Site-to-Site VPN")
        - VPCCustomerGateway("Primary PoP")
    )
    (
        tgw
        - Edge(label="failover vpn tgw attachment")
        - SiteToSiteVpn("Site-to-Site VPN")
        - VPCCustomerGateway("Failover PoP")
    )
    event = Eventbridge("Network-Manager-events")
    failover_lambda = LambdaFunction("VPN-Failover-Lambda")
    tgw_router_table = RouteTable("TGW-Route-Table")
    (
        tgw
        >> Edge(label="1. network manager")
        >> event
        >> Edge(label="2. tunnel status change")
        >> failover_lambda
        >> Edge(
            label="3. update static route 0.0.0.0 destination to primary/failover vpn tgw attachment"
        )
        >> tgw_router_table
    )

    tgw_router_table - Edge(style="dashed") - tgw
