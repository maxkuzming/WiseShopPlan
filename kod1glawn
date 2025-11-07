<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>WiseShopPlan</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: Arial, sans-serif;
      max-width: 700px;
      margin: 20px auto;
      padding: 0 15px;
      background: #fff;
      color: #333;
    }
    h1 { text-align: center; color: #2e8b57; margin: 20px 0; }
    h2 { text-align: center; margin: 20px 0; }
    .btn {
      display: inline-block;
      width: 90%;
      max-width: 300px;
      padding: 14px;
      margin: 10px 0;
      font-size: 16px;
      font-weight: bold;
      color: white;
      background: #8fbc8f;
      border: none;
      border-radius: 8px;
      cursor: pointer;
    }
    .btn:hover { background: #6f9c6f; }
    .back-btn { background: #556b2f; }
    .back-btn:hover { background: #455a24; }
    .view { text-align: center; display: none; }
    #main { display: block; }
    input {
      width: 90%;
      padding: 12px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 6px;
    }
    .recipe {
      background: #f9f9f9;
      padding: 16px;
      margin: 16px 0;
      border-radius: 10px;
      white-space: pre-wrap;
      line-height: 1.5;
    }
    .loading { color: #7f8c8d; text-align: center; font-style: italic; }
    .day {
      background: #e8f5e9;
      padding: 12px;
      margin: 12px 0;
      border-radius: 8px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h1>🛒 WiseShopPlan</h1>

  <!-- Главное меню -->
  <div id="main" class="view">
    <button class="btn" onclick="go('name')">По названию</button>
    <button class="btn" onclick="go('ingr')">Из того, что есть</button>
    <button class="btn" onclick="go('health')">Здоровое питание</button>
  </div>

  <!-- Поиск по названию -->
  <div id="name" class="view">
    <input id="q1" placeholder="Например: борщ с говядиной" />
    <button class="btn" onclick="s1()">Найти рецепт</button>
    <button class="btn back-btn" onclick="go('main')">В главное меню</button>
    <div id="r1"></div>
  </div>

  <!-- Поиск по ингредиентам -->
  <div id="ingr" class="view">
    <input id="q2" placeholder="Например: яйца, помидоры, лук" />
    <button class="btn" onclick="s2()">Что приготовить?</button>
    <button class="btn back-btn" onclick="go('main')">В главное меню</button>
    <div id="r2"></div>
  </div>

  <!-- Здоровое питание — Пн–Вс, завтрак/обед/ужин -->
  <div id="health" class="view">
    <h2>🥗 Здоровое питание (Пн–Вс)</h2>
    <div class="day">Понедельник<br>Завтрак: овсянка с ягодами и ложкой мёда<br>Обед: суп-пюре из брокколи + куриная грудка на пару<br>Ужин: творог с фруктами и орехами</div>
    <div class="day">Вторник<br>Завтрак: тост из цельнозернового хлеба с авокадо<br>Обед: салат из свежей капусты, моркови, с кусочком лосося<br>Ужин: запечённые овощи + тофу</div>
    <div class="day">Среда<br>Завтрак: гречневая каша с тыквой<br>Обед: чечевичный суп с зеленью<br>Ужин: йогурт без добавок + груша</div>
    <div class="day">Четверг<br>Завтрак: яичница из двух яиц с помидорами и шпинатом<br>Обед: бурый рис + тушёная индейка с кабачками<br>Ужин: кефир + горсть грецких орехов</div>
    <div class="day">Пятница<br>Завтрак: мюсли с йогуртом и бананом<br>Обед: салат из свёклы, грецких орехов и козьего сыра<br>Ужин: запечённая рыба + салат из огурцов и зелени</div>
    <div class="day">Суббота<br>Завтрак: рисовая каша с яблоком и корицей<br>Обед: овощной суп + кусочек цельнозернового хлеба<br>Ужин: творожная запеканка с ягодами</div>
    <div class="day">Воскресенье<br>Завтрак: омлет с овощами и зеленью<br>Обед: запечённая курица + картофель и брокколи<br>Ужин: ряженка + яблоко</div>
    <button class="btn back-btn" onclick="go('main')">В главное меню</button>
  </div>

  <script>
    const key = "YCPCqM2sdZa-cV8eQjfQgF5MOd8YzoyH1KXeVudY";
    const cat = "b1gk7vrlj4a3eqnv8ugg";

    function go(id) {
      document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
      document.getElementById(id).style.display = 'block';
    }

    async function ask(p) {
      const resp = await fetch('https://llm.api.cloud.yandex.net/foundationModels/v1/completion', {
        method: 'POST',
        headers: {
          'Authorization': `Api-Key ${key}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          modelUri: `gpt://${cat}/yandexgpt/latest`,
          completionOptions: { stream: false, temperature: 0.6, maxTokens: "2000" },
          messages: [{
            role: "system",
            text: "ты — дружелюбный повар-эксперт. отвечай строго по делу: сначала название блюда, затем список ингредиентов с мерами, затем пошаговый рецепт. пиши только на русском языке. без лишнего текста."
          }, {
            role: "user",
            text: p
          }]
        })
      });

      if (!resp.ok) throw new Error(`ошибка ${resp.status}`);
      const d = await resp.json();
      if (!d?.result?.alternatives?.[0]?.message?.text) throw new Error("нет ответа от ии");
      return d.result.alternatives[0].message.text;
    }

    async function s1() {
      const q = document.getElementById('q1').value.trim();
      const res = document.getElementById('r1');
      if (!q) return alert("введите название блюда");
      res.innerHTML = '<p class="loading">и и думает... ⏳</p>';
      try {
        const ans = await ask(`рецепт блюда: ${q}`);
        res.innerHTML = `<div class="recipe">${ans}</div>`;
      } catch (e) {
        res.innerHTML = `<p style="color:red;">❌ ${e.message}</p>`;
      }
    }

    async function s2() {
      const q = document.getElementById('q2').value.trim();
      const res = document.getElementById('r2');
      if (!q) return alert("введите ингредиенты");
      res.innerHTML = '<p class="loading">и и думает... ⏳</p>';
      try {
        const ans = await ask(`что приготовить из: ${q}? дай один подробный рецепт.`);
        res.innerHTML = `<div class="recipe">${ans}</div>`;
      } catch (e) {
        res.innerHTML = `<p style="color:red;">❌ ${e.message}</p>`;
      }
    }

    document.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        if (document.getElementById('name').style.display === 'block') s1();
        else if (document.getElementById('ingr').style.display === 'block') s2();
      }
    });
  </script>
</body>
</html>
