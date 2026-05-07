document.addEventListener('DOMContentLoaded', () => {
    // Nav logic
    const navBtns = document.querySelectorAll('.nav-btn');
    const modeSections = document.querySelectorAll('.mode-section');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const target = btn.dataset.target;
            modeSections.forEach(sec => {
                sec.style.display = sec.id === target ? 'block' : 'none';
            });
        });
    });

    // Populate strategies
    const stratSelects = ['opponent-strategy', 'sim-strat1', 'sim-strat2'];
    
    fetch('/api/strategies')
        .then(res => res.json())
        .then(data => {
            stratSelects.forEach(id => {
                const select = document.getElementById(id);
                for (const [key, name] of Object.entries(data)) {
                    const option = document.createElement('option');
                    option.value = key;
                    option.textContent = name;
                    select.appendChild(option);
                }
                if(id === 'sim-strat2') select.value = "2";
            });
        });

    // Interactive Game Logic
    const startBtn = document.getElementById('start-game-btn');
    const interactiveSetup = document.getElementById('interactive-setup');
    const interactiveGame = document.getElementById('interactive-game');
    const playerHand = document.getElementById('player-hand');
    const playerSlot = document.getElementById('player-played-card');
    const compSlot = document.getElementById('computer-played-card');
    const arenaMsg = document.getElementById('arena-message');
    
    startBtn.addEventListener('click', async () => {
        const stratId = document.getElementById('opponent-strategy').value;
        const numCards = document.getElementById('interactive-cards').value;
        const res = await fetch('/api/play/start', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ strategy_id: stratId, num_cards: numCards })
        });
        const data = await res.json();
        
        interactiveSetup.style.display = 'none';
        interactiveGame.style.display = 'block';
        updateGameState(data);
    });

    function updateGameState(data) {
        document.getElementById('player-score').textContent = data.player_score;
        document.getElementById('computer-score').textContent = data.opponent_score;
        document.getElementById('current-turn').textContent = data.turn;
        document.getElementById('total-turns').textContent = data.total_turns;

        // Render Hand
        playerHand.innerHTML = '';
        if(data.game_over) {
            arenaMsg.textContent = `Game Over! Final Winner: ${data.final_winner}`;
            playerSlot.textContent = '-';
            compSlot.textContent = '-';
            playerSlot.classList.remove('filled');
            compSlot.classList.remove('filled');
            
            // Add a restart button
            const restartBtn = document.createElement('button');
            restartBtn.className = 'primary-btn';
            restartBtn.textContent = 'Play Again';
            restartBtn.style.marginTop = '2rem';
            restartBtn.onclick = () => {
                interactiveSetup.style.display = 'block';
                interactiveGame.style.display = 'none';
                arenaMsg.textContent = 'Select a card to play';
                playerSlot.textContent = '?';
                compSlot.textContent = '?';
                playerSlot.classList.remove('filled');
                compSlot.classList.remove('filled');
            };
            playerHand.appendChild(restartBtn);
            return;
        }

        data.player_numbers.forEach(num => {
            const card = document.createElement('div');
            card.className = 'playing-card';
            card.textContent = num;
            card.onclick = () => playTurn(num);
            playerHand.appendChild(card);
        });
    }

    async function playTurn(choice) {
        playerHand.style.pointerEvents = 'none'; // Disable clicks
        
        // Optimistic UI for player
        playerSlot.textContent = choice;
        playerSlot.classList.add('filled');
        compSlot.textContent = '?';
        compSlot.classList.remove('filled');
        arenaMsg.textContent = 'Computer is thinking...';

        const res = await fetch('/api/play/turn', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ choice: choice })
        });
        const data = await res.json();

        // Reveal computer move
        setTimeout(() => {
            compSlot.textContent = data.turn_result.computer_played;
            compSlot.classList.add('filled');
            arenaMsg.textContent = data.turn_result.text;
            
            // Update state after small delay to show result
            setTimeout(() => {
                updateGameState(data);
                playerHand.style.pointerEvents = 'auto';
            }, 1500);
        }, 500);
    }

    // Simulation Logic
    const runSimBtn = document.getElementById('run-sim-btn');
    const simResults = document.getElementById('sim-results');
    
    runSimBtn.addEventListener('click', async () => {
        const s1 = document.getElementById('sim-strat1').value;
        const s2 = document.getElementById('sim-strat2').value;
        const games = document.getElementById('sim-games').value;
        const numCards = document.getElementById('sim-cards').value;
        
        runSimBtn.textContent = "Running...";
        runSimBtn.disabled = true;

        const res = await fetch('/api/simulate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ strat1_id: s1, strat2_id: s2, num_games: games, num_cards: numCards })
        });
        const data = await res.json();

        document.getElementById('res-p1-name').textContent = data.strat1_name;
        document.getElementById('res-p2-name').textContent = data.strat2_name;
        document.getElementById('res-p1-wins').textContent = data.player1_wins;
        document.getElementById('res-p2-wins').textContent = data.player2_wins;
        document.getElementById('res-ties').textContent = data.ties;

        const total = data.player1_wins + data.player2_wins + data.ties;
        document.getElementById('prog-p1').style.width = `${(data.player1_wins / total) * 100}%`;
        document.getElementById('prog-tie').style.width = `${(data.ties / total) * 100}%`;
        document.getElementById('prog-p2').style.width = `${(data.player2_wins / total) * 100}%`;

        simResults.style.display = 'block';
        runSimBtn.textContent = "Run Simulation";
        runSimBtn.disabled = false;
    });

    // Tournament Logic
    const runTourneyBtn = document.getElementById('run-tourney-btn');
    const tourneyResults = document.getElementById('tourney-results');
    const tourneyBody = document.getElementById('tourney-body');

    runTourneyBtn.addEventListener('click', async () => {
        const games = document.getElementById('tourney-games').value;
        const numCards = document.getElementById('tourney-cards').value;
        
        runTourneyBtn.textContent = "Running Tournament...";
        runTourneyBtn.disabled = true;

        const res = await fetch('/api/tournament', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ num_games: games, num_cards: numCards })
        });
        const data = await res.json();

        tourneyBody.innerHTML = '';
        data.forEach((row, idx) => {
            const tr = document.createElement('tr');
            const totalGames = row.wins + row.losses + row.ties;
            const winPct = ((row.wins / totalGames) * 100).toFixed(2);
            
            tr.innerHTML = `
                <td>${idx + 1}</td>
                <td>${row.strategy}</td>
                <td style="color: var(--accent); font-weight: 800;">${row.wins}</td>
                <td>${row.losses}</td>
                <td>${row.ties}</td>
                <td>${winPct}%</td>
            `;
            tourneyBody.appendChild(tr);
        });

        tourneyResults.style.display = 'block';
        runTourneyBtn.textContent = "Run Tournament";
        runTourneyBtn.disabled = false;
    });
});
