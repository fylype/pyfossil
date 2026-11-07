// ============================================================================
// Parâmetros da Geometria 
// ============================================================================
L = 10.0;     // Comprimento do domínio (direção X)
H = 5.0;      // Altura do domínio (direção Y)
R = 1.0;       // Raio do poço injetor (buraco) no centro

CX = L / 2.0;  // Coordenada X do centro
CY = H / 2.0;  // Coordenada Y do centro

// ============================================================================
// Parâmetros da Malha (Controle de Resolução)
// ============================================================================
lc_borda = 0.15;   // Tamanho dos elementos nas bordas externas
lc_poco  = 0.04;  // Tamanho dos elementos no contorno do poço (mais fino!)

// ============================================================================
// 1. Pontos do Retângulo Externo (Cantos e Pontos Médios)
// ============================================================================
Point(1) = {0, 0, 0, lc_borda}; // Canto Inferior Esquerdo
Point(2) = {L, 0, 0, lc_borda}; // Canto Inferior Direito
Point(3) = {L, H, 0, lc_borda}; // Canto Superior Direito
Point(4) = {0, H, 0, lc_borda}; // Canto Superior Esquerdo

// Pontos médios nas bordas (para podermos fazer os cortes)
Point(10) = {CX, 0, 0, lc_borda}; // Meio do Fundo
Point(11) = {L, CY, 0, lc_borda}; // Meio da Direita
Point(12) = {CX, H, 0, lc_borda}; // Meio do Topo
Point(13) = {0, CY, 0, lc_borda}; // Meio da Esquerda

// ============================================================================
// 2. Pontos e Arcos do Buraco Central (Poço Injetor)
// ============================================================================
Point(5) = {CX, CY, 0, lc_poco};     // Ponto Central (Referência)

Point(6) = {CX + R, CY, 0, lc_poco}; // Direita do buraco
Point(7) = {CX, CY + R, 0, lc_poco}; // Topo do buraco
Point(8) = {CX - R, CY, 0, lc_poco}; // Esquerda do buraco
Point(9) = {CX, CY - R, 0, lc_poco}; // Fundo do buraco

// ============================================================================
// 3. Linhas e Arcos
// ============================================================================
// Linhas do Retângulo Externo (divididas ao meio)
Line(1) = {1, 10}; // Fundo Esquerdo
Line(2) = {10, 2}; // Fundo Direito
Line(3) = {2, 11}; // Direita Inferior
Line(4) = {11, 3}; // Direita Superior
Line(5) = {3, 12}; // Topo Direito
Line(6) = {12, 4}; // Topo Esquerdo
Line(7) = {4, 13}; // Esquerda Superior
Line(8) = {13, 1}; // Esquerda Inferior

// Arcos circulares do Buraco
Circle(9)  = {6, 5, 7}; // Quadrante Superior Direito
Circle(10) = {7, 5, 8}; // Quadrante Superior Esquerdo
Circle(11) = {8, 5, 9}; // Quadrante Inferior Esquerdo
Circle(12) = {9, 5, 6}; // Quadrante Inferior Direito

// Cortes radiais (Ligando o buraco até as bordas do retângulo)
Line(13) = {6, 11}; // Corte Direita
Line(14) = {7, 12}; // Corte Topo
Line(15) = {8, 13}; // Corte Esquerda
Line(16) = {9, 10}; // Corte Fundo

// ============================================================================
// 4. Definição das Superfícies (Os 4 Quadrantes/Materiais)
// O sinal de menos (-) indica que a linha está sendo percorrida no sentido inverso
// ============================================================================

// Quadrante 1: Superior Direito
Curve Loop(1) = {13, 4, 5, -14, -9}; 
Plane Surface(1) = {1};

// Quadrante 2: Superior Esquerdo
Curve Loop(2) = {14, 6, 7, -15, -10}; 
Plane Surface(2) = {2};

// Quadrante 3: Inferior Esquerdo
Curve Loop(3) = {15, 8, 1, -16, -11}; 
Plane Surface(3) = {3};

// Quadrante 4: Inferior Direito
Curve Loop(4) = {16, 2, 3, -13, -12}; 
Plane Surface(4) = {4};

// ============================================================================
// 5. Configurações da Malha (Forçando Quadriláteros)
// ============================================================================
Recombine Surface {1, 2, 3, 4};

// ============================================================================
// 6. GRUPOS FÍSICOS (Physical Groups)
// ============================================================================

// A) Condições de Contorno (Cada borda original agora possui 2 linhas)
Physical Curve("Bottom_NoFlow", 1) = {1, 2};
Physical Curve("Right_Open", 2)    = {3, 4};
Physical Curve("Top_NoFlow", 3)    = {5, 6};
Physical Curve("Left_Open", 4)     = {7, 8};
Physical Curve("Injection_Hole", 5)= {9, 10, 11, 12};

// B) Material IDs 
// O deal.II vai ler essas partições como se fossem rochas de características diferentes
Physical Surface("Reservoir_Mat_1", 1) = {1}; // Quadrante Superior Direito
Physical Surface("Reservoir_Mat_2", 2) = {2}; // Quadrante Superior Esquerdo
Physical Surface("Reservoir_Mat_3", 3) = {3}; // Quadrante Inferior Esquerdo
Physical Surface("Reservoir_Mat_4", 4) = {4}; // Quadrante Inferior Direito
