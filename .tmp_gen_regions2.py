import os
base = os.environ["USERPROFILE"] + "\\Documents\\CAAC考证报名网站"
p = base + "\\js\\regions.js"
# Read existing R data from the file
d = open(p, "r", encoding="utf-8").read()
# Extract R data (everything before the first function)
idx = d.find("function updateCities")
r_data = d[:idx].rstrip(";") + ";"

# Build the rest of the file
funcs = r"""

function updateCities(t) {
  var p = t.value;
  var c = document.getElementById(t.id.replace("province","city"));
  c.innerHTML = '<option value="">-- \u8bf7\u9009\u62e9\u5e02 --</option>';
  var d = document.getElementById(t.id.replace("province","district"));
  d.innerHTML = '<option value="">-- \u8bf7\u9009\u62e9\u533a --</option>';
  if (!p || !R[p]) return;
  var cities = Object.keys(R[p]);
  for (var i = 0; i < cities.length; i++) {
    c.innerHTML += '<option value="' + cities[i] + '">' + cities[i] + '</option>';
  }
}

function updateDistricts(t) {
  var c = t.value;
  var pSel = document.getElementById(t.id.replace("city","province"));
  var d = document.getElementById(t.id.replace("city","district"));
  d.innerHTML = '<option value="">-- \u8bf7\u9009\u62e9\u533a --</option>';
  if (!c || !pSel.value || !R[pSel.value]) return;
  var districts = R[pSel.value][c];
  if (!districts) return;
  for (var i = 0; i < districts.length; i++) {
    d.innerHTML += '<option value="' + districts[i] + '">' + districts[i] + '</option>';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var provinces = Object.keys(R);
  var sels = document.querySelectorAll('select[name="province"]');
  for (var i = 0; i < sels.length; i++) {
    var sel = sels[i];
    for (var j = 0; j < provinces.length; j++) {
      var opt = document.createElement("option");
      opt.value = provinces[j];
      opt.textContent = provinces[j];
      sel.appendChild(opt);
    }
  }
});
"""

open(p, "w", encoding="utf-8").write(r_data + funcs)
print("regions.js rewritten: %d lines" % (r_data.count("\n") + funcs.count("\n")))
