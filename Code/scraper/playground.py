from main import _GetSpecifications, append_dict_to_json

output = _GetSpecifications('https://www.homedepot.com/p/Frigidaire-Gallery-24-4375-in-Width-2-2-cu-ft-Stainless-Steel-1100-Watt-Built-In-Microwave-GMBS3068AF/320574931')
print(output)
append_dict_to_json(output, 'playground.json')

output = _GetSpecifications('https://www.homedepot.com/p/Sharp-1-2-cu-ft-Microwave-Drawer-in-Stainless-Steel-SMD2489ES/312482370')
print(output)
append_dict_to_json(output, 'playground.json')