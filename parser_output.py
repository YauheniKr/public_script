import textfsm
import re
from tabulate import tabulate

template = 'template.txt'
output = ['MBH-GO_Rogach-Lunach10-6150-1#terminal length 0\r\nMBH-GO_Rogach-Lunach10-6150-1#show interface description\r\nInterface                       AdminStatus  PhyStatus  Protocol  Description\r\ngei-1/1/0/1                     up           up         up        RRL-Management\r\ngei-1/1/0/2                     down         down       down      TN\r\ngei-1/1/0/3                     up           down       down      \r\ngei-1/1/0/4                     up           up         up        \r\ngei-1/1/0/5                     up           up         up        MLTN_ETU3_TR1\r\ngei-1/1/0/6                     up           down       down      \r\ngei-1/1/0/7                     up           down       down      \r\ngei-1/1/0/8                     up           down       down      \r\ngei-1/2/0/1                     up           up         up        MLTN_AMM3_ETU3\r\n                                                                  _TR2\r\ngei-1/2/0/2                     up           up         up        SHP-H309-1910_\r\n                                                                  Gi1/0/20\r\ngei-1/2/0/3                     down         down       down      \r\ngei-1/2/0/4                     up           up         up        L2VPN_to_GOMEL\r\n                                                                  _CS1\r\ngei-1/2/0/4.2103                up           up         up        \r\ngei-1/2/0/5                     up           up         up        Eltek\r\ngei-1/2/0/6                     up           up         up        Eltek\r\ngei-1/2/0/6.2104                up           up         up        \r\ngei-1/2/0/7                     up           down       down      \r\ngei-1/2/0/8                     up           down       down      \r\nxgei-1/5/0/1                    up           down       down      \r\nxgei-1/5/0/2                    up           down       down      \r\nxgei-1/6/0/1                    up           down       down      \r\nxgei-1/6/0/2                    up           down       down      \r\nloopback1                       up           up         up        \r\nloopback1023                    up           up         up        \r\nvlan1                           down         up         down      \r\nvlan1100                        up           up         up        Shop_Rogachev_\r\n                                                                  Lenina-49a\r\nvlan2031                        up           up         up        2G_ZTE_Abis\r\nvlan2400                        up           up         up        Power monitori\r\n                                                                  ng\r\nvlan2603                        up           up         up        RRL OAM\r\nvlan2604                        down         up         down      RRL-Management\r\nvlan2732                        up           up         up        \r\nvlan3100                        up           up         up        RRL_Reserve\r\nvlan3999                        up           up         down      \r\nsmartgroup1                     up           up         up        MLTN_ETU3_(TR1\r\n                                                                  +TR2)\r\nMBH-GO_Rogach-Lunach10-6150-1#', 'MBH-GO-Mozyr-6150-1#terminal length 0\r\nMBH-GO-Mozyr-6150-1#show interface description\r\nInterface                       AdminStatus  PhyStatus  Protocol  Description\r\ngei-1/1/0/1                     up           down       down      MOZYR 1,4,7,8,\r\n                                                                  11, NPZ,MOZRM1\r\ngei-1/1/0/2                     up           down       down      RRL-Management\r\ngei-1/1/0/3                     up           up         up        Enatel SM32\r\ngei-1/1/0/4                     up           up         up        l2_interconnec\r\n                                                                  t_to_2-nd_ASR \r\n                                                                  gei-1/1/0/4\r\ngei-1/1/0/4.2604                up           up         up        \r\ngei-1/1/0/4.3104                up           up         up        \r\ngei-1/1/0/4.4004                up           up         up        OSPF30 INTERCO\r\n                                                                  NN\r\ngei-1/1/0/5                     up           up         up        L2VPN_to_mbh-g\r\n                                                                  ml-7609cs-1 ge\r\n                                                                  i-1/1/0/5\r\ngei-1/1/0/5.2105                up           up         up        to mbh-gml-760\r\n                                                                  9cs-1\r\ngei-1/1/0/6                     up           up         up        l3_interconnec\r\n                                                                  t_to_2-nd_ASR \r\n                                                                  gei-1/1/0/6\r\ngei-1/1/0/7                     up           up         up        REP10-to-MBH-G\r\n                                                                  O-MOZYR8-Gagar\r\n                                                                  93 gei-1/1/0/7\r\ngei-1/1/0/8                     up           down       down      \r\nxgei-1/5/0/1                    up           down       down      \r\nxgei-1/5/0/2                    up           down       down      \r\nxgei-1/6/0/1                    up           down       down      \r\nxgei-1/6/0/2                    up           down       down      \r\nloopback1                       up           up         up        \r\nloopback30                      up           up         up        OSPF30 RID\r\nloopback1023                    up           up         up        \r\nvlan2020                        up           up         up        2G_ZTE_Abis\r\nvlan2120                        up           up         down      Abis\r\nvlan2130                        up           up         down      IuB\r\nvlan2400                        up           up         up        Power monitori\r\n                                                                  ng\r\nvlan2401                        up           up         up        Service\r\nvlan2721                        up           up         up        3G_ZTE_IuB\r\nvlan2799                        up           up         up        \r\nMBH-GO-Mozyr-6150-1#', 'MBH-GO-Mozyr-6150-2#terminal length 0\r\nMBH-GO-Mozyr-6150-2#show interface description\r\nInterface                       AdminStatus  PhyStatus  Protocol  Description\r\ngei-1/1/0/1                     up           down       down      Protection for\r\n                                                                   TN\r\ngei-1/1/0/2                     up           up         up        l2_interconnec\r\n                                                                  t_to_1-st_ASR\r\ngei-1/1/0/2.3104                up           up         up        Mozyr_Kalinkov\r\n                                                                  ochi_RRL_Reser\r\n                                                                  ve\r\ngei-1/1/0/2.4004                up           up         up        OSPF30 INTERCO\r\n                                                                  NN\r\ngei-1/1/0/3                     down         down       down      \r\ngei-1/1/0/4                     up           up         up        L2VPN_to_mbh-g\r\n                                                                  ml-7609cs-2\r\ngei-1/1/0/4.2106                up           up         up        \r\ngei-1/1/0/5                     up           up         up        l3_interconnec\r\n                                                                  t_to_1-st_ASR\r\ngei-1/1/0/6                     up           up         up        REP10-to-MBH-G\r\n                                                                  O-MOZYR7-Berez\r\n                                                                  4\r\ngei-1/1/0/7                     up           up         up        MOZR19\r\ngei-1/1/0/8                     up           down       down      \r\nxgei-1/5/0/1                    up           down       down      \r\nxgei-1/5/0/2                    up           down       down      \r\nxgei-1/6/0/1                    up           down       down      \r\nxgei-1/6/0/2                    up           down       down      \r\nloopback1                       up           up         up        \r\nloopback30                      up           up         up        OSPF30 RID\r\nloopback755                     up           up         up        \r\nloopback1023                    up           up         up        \r\nvlan2020                        up           up         up        2G_ZTE_Abis\r\nvlan2120                        up           up         up        Abis\r\nvlan2130                        up           up         up        IuB\r\nvlan2400                        up           up         up        Power monitori\r\n                                                                  ng\r\nvlan2401                        up           up         up        Service\r\nvlan2721                        up           up         up        3G_ZTE_IuB\r\nvlan2799                        up           up         up        \r\nMBH-GO-Mozyr-6150-2#']
def parser_show_interface_description (output, template):
    result = []
    f = open(template)
    re_table = textfsm.TextFSM(f)
    result_header = re_table.header
    result.append(result_header)
    result_output = re_table.ParseText(output)
    result.extend(result_output)
    return result


test = re.sub('(\r\n {66})', '', ''.join(output))
listing = parser_show_interface_description(test, template)
print(tabulate(listing[1:], headers=listing[0]))
