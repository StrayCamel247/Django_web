window.onkeydown = (
		    (ctx, snake, food, direction, move, draw) => (
		        (loop, newFood, timer) =>
                    Array.from({length : 400}).forEach((_e, i) => draw(ctx, i, "#dddddd"))
                    ||(
		                timer = setInterval(() =>
                            loop(newFood)
                            || clearInterval(timer)
                            || console.log(timer)
                            || alert('游戏结束  Game Over'), 200)
                    )

                    &&(
                        e => direction =
                            snake[1] - snake[0] ===
                                (move = [-1,-20,1,20][(e || event).keyCode - 37] || direction) ? direction : move
                    )
            )
            (
                (newFood) =>
                    snake.unshift( move = snake[0] + direction)
                    && snake.indexOf(move,1) > 0
                    || move < 0 || move > 399
                    || direction === 1 && move % 20 === 0
                    || direction === -1
                    && move % 20 === 19 ? false : (draw(ctx, move, "green")
                    || move === food ? newFood() & draw(ctx, food, "red") : draw(ctx, snake.pop(), "#dddddd")) !== [],

                () =>
                    Array.from({length : 8000}).some(e =>
                        snake.indexOf(food = ~~(Math.random()*400)) === -1)
            )
)

(
    document.getElementById('canvas').getContext('2d'),
    [42, 41],
    43,
    1,
    null,
    (ctx, node, color) =>
        (ctx.fillStyle=color) & ctx.fillRect(node%20*20+1,~~(node/20)*20+1,18,18)
);
