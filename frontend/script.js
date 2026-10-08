// script.js - chat and lawyers logic (static)

// --------------------- CHAT ---------------------
window.initChat = function () {
  const form = document.getElementById('chatForm');
  const input = document.getElementById('userInput');
  const win = document.getElementById('chatWindow');

  form && form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    input.value = '';
    appendMessage('Thinking...', 'bot');

    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });

      if (!res.ok) throw new Error('Server ' + res.status);

      const data = await res.json();

      // remove thinking message
      const bots = Array.from(win.querySelectorAll('.msg.bot'));
      const last = bots[bots.length - 1];
      if (last && last.textContent.includes('Thinking')) last.remove();

      const reply =
        data.answer ||
        (data.result && data.result.answer) ||
        JSON.stringify(data);

      appendMessage(reply, 'bot');

    } catch (err) {
      appendMessage('Error: ' + err.message, 'bot');
    }
  });

  function appendMessage(text, who) {
    const div = document.createElement('div');
    div.className = 'msg ' + (who === 'user' ? 'user' : 'bot');

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = '⚖️';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = text;

    div.appendChild(avatar);
    div.appendChild(bubble);

    win.appendChild(div);
    win.scrollTop = win.scrollHeight;
  }
};



// --------------------- LAWYERS ---------------------
window.renderLawyers = function () {

  const lawyers = [
    {
      name: 'Adv. Rajesh Sharma',
      initial: 'RS',
      domain: 'Criminal Law',
      location: 'Mumbai, Maharashtra',
      rating: '4.9',
      exp: '18 years',
      phone: '+91 98231 44567',
      bio: 'Specialist in criminal trials, bail matters, white-collar crimes, and FIR quashing.'
    },

    {
      name: 'Adv. Priya Mehta',
      initial: 'PM',
      domain: 'Family Law',
      location: 'Ahmedabad, Gujarat',
      rating: '4.8',
      exp: '12 years',
      phone: '+91 90995 88772',
      bio: 'Experienced in divorce cases, child custody, domestic violence, and mediation.'
    },

    {
      name: 'Adv. Arjun Verma',
      initial: 'AV',
      domain: 'Cyber Law',
      location: 'Bengaluru, Karnataka',
      rating: '4.7',
      exp: '9 years',
      phone: '+91 97455 22110',
      bio: 'Handles cyber fraud, online harassment, hacking disputes, and data protection cases.'
    },

    {
      name: 'Adv. Neha Kulkarni',
      initial: 'NK',
      domain: 'Corporate Law',
      location: 'Pune, Maharashtra',
      rating: '4.9',
      exp: '14 years',
      phone: '+91 88067 43012',
      bio: 'Expert in business contracts, mergers & acquisitions, startup compliance, and taxation.'
    },

    {
      name: 'Adv. Sandeep Reddy',
      initial: 'SR',
      domain: 'Property & Real Estate Law',
      location: 'Hyderabad, Telangana',
      rating: '4.8',
      exp: '11 years',
      phone: '+91 99895 11234',
      bio: 'Handles property disputes, registration, land verification, and RERA matters.'
    }
  ];

  const grid = document.getElementById('lawyerGrid');
  if (!grid) return;

  grid.innerHTML = '';

  lawyers.forEach(l => {
    const card = document.createElement('article');
    card.className = 'lawyer-card';

    card.innerHTML = `
      <div class="card-row">
        <div class="initial">${l.initial}</div>
        <div>
          <h3 style="margin:0">${l.name}</h3>
          <div class="muted" style="margin-top:6px">${l.domain}</div>
          <div class="muted" style="margin-top:6px">${l.location}</div>
        </div>
      </div>

      <div class="rating" style="margin-top:12px; font-size:14px;">
        ⭐ <strong>${l.rating}</strong> &nbsp; • &nbsp; <span>${l.exp} experience</span>
      </div>

      <div class="phone" style="margin-top:6px; color:#e0aa2a; font-size:15px;">
        📞 <strong>${l.phone}</strong>
      </div>

      <p class="muted" style="margin-top:12px">${l.bio}</p>

      <div class="card-actions">
        <button class="btn primary" style="width:100%;">Connect</button>
      </div>
    `;

    grid.appendChild(card);
  });


  // Search functionality  
  const search = document.getElementById('search');
  if (search) {
    search.addEventListener('input', () => {
      const q = search.value.toLowerCase();
      grid.querySelectorAll('.lawyer-card').forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(q)
          ? 'block'
          : 'none';
      });
    });
  }
};
