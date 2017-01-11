# Supply and Demand Test

t = TikZPicture()
t.addAx(11, 11, xlabel="Quantity", ylabel="Price")

t.addLine([(2,2), (10,10)])
t.addLine([(2,10), (10,2)])
t.addLine([(0,6), (6,6)], options=['dashed'])
t.addLine([(6,0), (6,6)], options=['dashed'])

t.addLabel((11,10), "Supply")
t.addLabel((11,2), "Demand")

t.addPoint((0,6), "$p^*$", nodeOptions=['left'])
t.addPoint((6,0), "$q^*$", nodeOptions=['below'])

print(t.build())

# Indifference Curve Test

t = TikZPicture()
t.addAx(11, 11, xlabel="Peas", ylabel="Carrots")

t.addLine([(0,8), (8,0)], options=['dashed'])
t.addLine([(2,10), (4,4), (10,2)], options=['smooth'], angles=[(-90,135), (-45,180)])

t.addPoint((0,8), "$\\frac{Y}{p_c}$", nodeOptions=['left'])
t.addPoint((8,0), "$\\frac{Y}{p_p}$", nodeOptions=['below'])

t.addPoint((4,4), "$(q_p^*,q_c^*)$", nodeOptions=['above right'])

print(t.build())

# Solow Growth Model Test

t = TikZPicture()
t.addAx(11, 11, xlabel="$k$", ylabel="")

t.addPlot("4.5*ln(\\x+1)", [0,10]) # income
t.addPlot("3*ln(\\x+1)", [0,10])   # investment
t.addLine([(0,0), (10,10)])        # depreciation

t.addLine([(5.711,0), (5.711,10)], options=['dashed'])
t.addLabel((5.711,0), "$k^*$", options=['below'])

t.addLabel((10,10), "$(n+g+\delta)k$", options=['right'])
t.addLabel((10,10.8), "$f(k)$", options=['right'])
t.addLabel((10,7.12), "$sf(k)$", options=['right'])

print(t.build())
