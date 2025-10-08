const lgas = {
  "Abia": ["Aba North", "Aba South", "Umuahia North", "Umuahia South"],
  "Adamawa": ["Yola North", "Yola South", "Mubi North", "Mubi South"],
  "Akwa Ibom": ["Uyo", "Eket", "Ikot Ekpene"],
  "Anambra": ["Awka South", "Onitsha North", "Onitsha South"],
  "Bauchi": ["Bauchi", "Katagum", "Misau"],
  "Bayelsa": ["Yenagoa", "Ogbia", "Sagbama"],
  "Benue": ["Makurdi", "Gboko", "Otukpo"],
  "Borno": ["Maiduguri", "Biu", "Dikwa"],
  "Cross River": ["Calabar South", "Odukpani", "Ikom"],
  "Delta": ["Warri South", "Asaba", "Ughelli North"],
  "Ebonyi": ["Abakaliki", "Afikpo North", "Ohaozara"],
  "Edo": ["Benin City", "Esan West", "Oredo"],
  "Ekiti": ["Ado Ekiti", "Ikere", "Ijero"],
  "Enugu": ["Enugu North", "Enugu South", "Nsukka"],
  "FCT": ["Abaji", "AMAC", "Bwari", "Gwagwalada", "Kuje", "Kwali"],
  "Gombe": ["Gombe", "Billiri", "Kaltungo"],
  "Imo": ["Owerri Municipal", "Okigwe", "Orlu"],
  "Jigawa": ["Dutse", "Hadejia", "Kazaure"],
  "Kaduna": ["Kaduna North", "Kaduna South", "Zaria"],
  "Kano": ["Tarauni", "Nasarawa", "Gwale"],
  "Katsina": ["Katsina", "Daura", "Funtua"],
  "Kebbi": ["Birnin Kebbi", "Argungu", "Yauri"],
  "Kogi": ["Lokoja", "Okene", "Idah"],
  "Kwara": ["Ilorin East", "Ilorin West", "Offa"],
  "Lagos": ["Ikeja", "Surulere", "Epe", "Eti-Osa"],
  "Nasarawa": ["Lafia", "Keffi", "Akwanga"],
  "Niger": ["Minna", "Bida", "Suleja", "Paikoro"],
  "Ogun": ["Abeokuta North", "Ado Odo/Ota", "Ijebu Ode"],
  "Ondo": ["Akure South", "Owo", "Ondo East"],
  "Osun": ["Osogbo", "Ife Central", "Ilesha West"],
  "Oyo": ["Ibadan North", "Ogbomosho North", "Oyo East"],
  "Plateau": ["Jos North", "Jos South", "Barkin Ladi"],
  "Rivers": ["Port Harcourt", "Obio/Akpor", "Bonny"],
  "Sokoto": ["Sokoto North", "Sokoto South", "Wurno"],
  "Taraba": ["Jalingo", "Bali", "Wukari"],
  "Yobe": ["Damaturu", "Nguru", "Potiskum"],
  "Zamfara": ["Gusau", "Kaura Namoda", "Anka"]
};

function updateLGA() {
  const state = document.getElementById('state').value;
  const lgaSelect = document.getElementById('lga');
  lgaSelect.innerHTML = '<option value="">Select LGA</option>';
  if (lgas[state]) {
    lgas[state].forEach(lga => {
      const option = document.createElement('option');
      option.value = lga;
      option.textContent = lga;
      lgaSelect.appendChild(option);
    });
  }
}
