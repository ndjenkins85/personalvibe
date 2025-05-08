(personalvibe-py3.12) bash-3.2$ npm install
npm error code ETARGET
npm error notarget No matching version found for @types/react-router-dom@^6.23.1.
npm error notarget In most cases you or one of your dependencies are requesting
npm error notarget a package version that doesn't exist.
npm notice
npm notice New major version of npm available! 10.9.2 -> 11.3.0
npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.3.0
npm notice To update run: npm install -g npm@11.3.0
npm notice
npm error A complete log of this run can be found in: /Users/nicholasjenkins/.npm/_logs/2025-05-08T17_22_10_203Z-debug-0.log
(personalvibe-py3.12) bash-3.2$

0 verbose cli /Users/nicholasjenkins/.nvm/versions/node/v22.15.0/bin/node /Users/nicholasjenkins/.nvm/versions/node/v22.15.0/bin/npm
1 info using npm@10.9.2
2 info using node@v22.15.0
3 silly config load:file:/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/npmrc
4 silly config load:file:/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/.npmrc
5 silly config load:file:/Users/nicholasjenkins/.npmrc
6 silly config load:file:/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/etc/npmrc
7 verbose title npm install
8 verbose argv "install"
9 verbose logfile logs-max:10 dir:/Users/nicholasjenkins/.npm/_logs/2025-05-08T17_22_10_203Z-
10 verbose logfile /Users/nicholasjenkins/.npm/_logs/2025-05-08T17_22_10_203Z-debug-0.log
11 silly logfile done cleaning log files
12 silly packumentCache heap:4345298944 maxSize:1086324736 maxEntrySize:543162368
13 silly idealTree buildDeps
14 silly fetch manifest react@^18.3.0
15 silly packumentCache full:https://registry.npmjs.org/react cache-miss
16 http fetch GET 200 https://registry.npmjs.org/react 655ms (cache miss)
17 silly packumentCache full:https://registry.npmjs.org/react set size:undefined disposed:false
18 silly fetch manifest react-dom@^18.3.0
19 silly packumentCache full:https://registry.npmjs.org/react-dom cache-miss
20 http fetch GET 200 https://registry.npmjs.org/npm 940ms
21 http fetch GET 200 https://registry.npmjs.org/react-dom 441ms (cache miss)
22 silly packumentCache full:https://registry.npmjs.org/react-dom set size:undefined disposed:false
23 silly fetch manifest react-router-dom@^6.23.0
24 silly packumentCache full:https://registry.npmjs.org/react-router-dom cache-miss
25 http fetch GET 200 https://registry.npmjs.org/react-router-dom 198ms (cache miss)
26 silly packumentCache full:https://registry.npmjs.org/react-router-dom set size:undefined disposed:false
27 silly fetch manifest @types/react@^18.2.24
28 silly packumentCache full:https://registry.npmjs.org/@types%2freact cache-miss
29 http fetch GET 200 https://registry.npmjs.org/@types%2freact 146ms (cache miss)
30 silly packumentCache full:https://registry.npmjs.org/@types%2freact set size:undefined disposed:false
31 silly fetch manifest @types/react-dom@^18.2.9
32 silly packumentCache full:https://registry.npmjs.org/@types%2freact-dom cache-miss
33 http fetch GET 200 https://registry.npmjs.org/@types%2freact-dom 134ms (cache miss)
34 silly packumentCache full:https://registry.npmjs.org/@types%2freact-dom set size:undefined disposed:false
35 silly fetch manifest @types/react-router-dom@^6.23.1
36 silly packumentCache full:https://registry.npmjs.org/@types%2freact-router-dom cache-miss
37 http fetch GET 200 https://registry.npmjs.org/@types%2freact-router-dom 232ms (cache miss)
38 silly packumentCache full:https://registry.npmjs.org/@types%2freact-router-dom set size:undefined disposed:false
39 silly fetch manifest @vitejs/plugin-react@^4.2.1
40 silly packumentCache full:https://registry.npmjs.org/@vitejs%2fplugin-react cache-miss
41 http fetch GET 200 https://registry.npmjs.org/@vitejs%2fplugin-react 121ms (cache miss)
42 silly packumentCache full:https://registry.npmjs.org/@vitejs%2fplugin-react set size:undefined disposed:false
43 silly fetch manifest vite@^5.2.10
44 silly packumentCache full:https://registry.npmjs.org/vite cache-miss
45 http fetch GET 200 https://registry.npmjs.org/vite 1755ms (cache miss)
46 silly packumentCache full:https://registry.npmjs.org/vite set size:undefined disposed:false
47 silly fetch manifest @types/node@^18.0.0 || >=20.0.0
48 silly packumentCache full:https://registry.npmjs.org/@types%2fnode cache-miss
49 http fetch GET 200 https://registry.npmjs.org/@types%2fnode 483ms (cache miss)
50 silly packumentCache full:https://registry.npmjs.org/@types%2fnode set size:undefined disposed:false
51 silly fetch manifest less@*
52 silly packumentCache full:https://registry.npmjs.org/less cache-miss
53 http fetch GET 200 https://registry.npmjs.org/less 89ms (cache miss)
54 silly packumentCache full:https://registry.npmjs.org/less set size:undefined disposed:false
55 silly fetch manifest lightningcss@^1.21.0
56 silly packumentCache full:https://registry.npmjs.org/lightningcss cache-miss
57 http fetch GET 200 https://registry.npmjs.org/lightningcss 62ms (cache miss)
58 silly packumentCache full:https://registry.npmjs.org/lightningcss set size:undefined disposed:false
59 silly fetch manifest sass@*
60 silly packumentCache full:https://registry.npmjs.org/sass cache-miss
61 http fetch GET 200 https://registry.npmjs.org/sass 142ms (cache miss)
62 silly packumentCache full:https://registry.npmjs.org/sass set size:undefined disposed:false
63 silly fetch manifest sass-embedded@*
64 silly packumentCache full:https://registry.npmjs.org/sass-embedded cache-miss
65 http fetch GET 200 https://registry.npmjs.org/sass-embedded 75ms (cache miss)
66 silly packumentCache full:https://registry.npmjs.org/sass-embedded set size:undefined disposed:false
67 silly fetch manifest stylus@*
68 silly packumentCache full:https://registry.npmjs.org/stylus cache-miss
69 http fetch GET 200 https://registry.npmjs.org/stylus 98ms (cache miss)
70 silly packumentCache full:https://registry.npmjs.org/stylus set size:undefined disposed:false
71 silly fetch manifest sugarss@*
72 silly packumentCache full:https://registry.npmjs.org/sugarss cache-miss
73 http fetch GET 200 https://registry.npmjs.org/sugarss 76ms (cache miss)
74 silly packumentCache full:https://registry.npmjs.org/sugarss set size:undefined disposed:false
75 silly fetch manifest postcss@^8.3.3
76 silly packumentCache full:https://registry.npmjs.org/postcss cache-miss
77 http fetch GET 200 https://registry.npmjs.org/postcss 122ms (cache miss)
78 silly packumentCache full:https://registry.npmjs.org/postcss set size:undefined disposed:false
79 silly fetch manifest terser@^5.4.0
80 silly packumentCache full:https://registry.npmjs.org/terser cache-miss
81 http fetch GET 200 https://registry.npmjs.org/terser 122ms (cache miss)
82 silly packumentCache full:https://registry.npmjs.org/terser set size:undefined disposed:false
83 silly fetch manifest typescript@^5.4.5
84 silly packumentCache full:https://registry.npmjs.org/typescript cache-miss
85 http fetch GET 200 https://registry.npmjs.org/typescript 856ms (cache miss)
86 silly packumentCache full:https://registry.npmjs.org/typescript set size:undefined disposed:false
87 silly placeDep ROOT @types/react@18.3.21 OK for: storymaker-spa@0.0.1 want: ^18.2.24
88 silly placeDep ROOT @types/react-dom@18.3.7 OK for: storymaker-spa@0.0.1 want: ^18.2.9
89 silly placeDep ROOT @types/react-router-dom@ OK for: storymaker-spa@0.0.1 want: ^6.23.1
90 silly placeDep ROOT @vitejs/plugin-react@4.4.1 OK for: storymaker-spa@0.0.1 want: ^4.2.1
91 silly placeDep ROOT vite@5.4.19 OK for: @vitejs/plugin-react@4.4.1 want: ^4.2.0 || ^5.0.0 || ^6.0.0
92 silly placeDep ROOT react@18.3.1 OK for: storymaker-spa@0.0.1 want: ^18.3.0
93 silly placeDep ROOT react-dom@18.3.1 OK for: storymaker-spa@0.0.1 want: ^18.3.0
94 silly placeDep ROOT react-router-dom@6.30.0 OK for: storymaker-spa@0.0.1 want: ^6.23.0
95 silly placeDep ROOT typescript@5.8.3 OK for: storymaker-spa@0.0.1 want: ^5.4.5
96 silly fetch manifest csstype@^3.0.2
97 silly packumentCache full:https://registry.npmjs.org/csstype cache-miss
98 silly fetch manifest @types/prop-types@*
99 silly packumentCache full:https://registry.npmjs.org/@types%2fprop-types cache-miss
100 silly fetch manifest @babel/core@^7.26.10
101 silly packumentCache full:https://registry.npmjs.org/@babel%2fcore cache-miss
102 silly fetch manifest @babel/plugin-transform-react-jsx-self@^7.25.9
103 silly packumentCache full:https://registry.npmjs.org/@babel%2fplugin-transform-react-jsx-self cache-miss
104 silly fetch manifest @babel/plugin-transform-react-jsx-source@^7.25.9
105 silly packumentCache full:https://registry.npmjs.org/@babel%2fplugin-transform-react-jsx-source cache-miss
106 silly fetch manifest @types/babel__core@^7.20.5
107 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__core cache-miss
108 silly fetch manifest react-refresh@^0.17.0
109 silly packumentCache full:https://registry.npmjs.org/react-refresh cache-miss
110 http fetch GET 200 https://registry.npmjs.org/@types%2fprop-types 95ms (cache miss)
111 silly packumentCache full:https://registry.npmjs.org/@types%2fprop-types set size:undefined disposed:false
112 silly fetch manifest rollup@^4.20.0
113 silly packumentCache full:https://registry.npmjs.org/rollup cache-miss
114 http fetch GET 200 https://registry.npmjs.org/csstype 96ms (cache miss)
115 silly packumentCache full:https://registry.npmjs.org/csstype set size:undefined disposed:false
116 silly fetch manifest esbuild@^0.21.3
117 silly packumentCache full:https://registry.npmjs.org/esbuild cache-miss
118 http fetch GET 200 https://registry.npmjs.org/@types%2fbabel__core 230ms (cache miss)
119 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__core set size:undefined disposed:false
120 silly fetch manifest postcss@^8.4.43
121 silly packumentCache full:https://registry.npmjs.org/postcss cache-miss
122 http cache https://registry.npmjs.org/postcss 10ms (cache hit)
123 silly packumentCache full:https://registry.npmjs.org/postcss set size:687240 disposed:false
124 silly fetch manifest fsevents@~2.3.3
125 silly packumentCache full:https://registry.npmjs.org/fsevents cache-miss
126 http fetch GET 200 https://registry.npmjs.org/@babel%2fplugin-transform-react-jsx-source 271ms (cache miss)
127 silly packumentCache full:https://registry.npmjs.org/@babel%2fplugin-transform-react-jsx-source set size:undefined disposed:false
128 silly fetch manifest loose-envify@^1.1.0
129 silly packumentCache full:https://registry.npmjs.org/loose-envify cache-miss
130 http fetch GET 200 https://registry.npmjs.org/fsevents 79ms (cache miss)
131 silly packumentCache full:https://registry.npmjs.org/fsevents set size:undefined disposed:false
132 silly fetch manifest scheduler@^0.23.2
133 silly packumentCache full:https://registry.npmjs.org/scheduler cache-miss
134 http fetch GET 200 https://registry.npmjs.org/loose-envify 59ms (cache miss)
135 silly packumentCache full:https://registry.npmjs.org/loose-envify set size:undefined disposed:false
136 silly fetch manifest react-router@6.30.0
137 silly packumentCache full:https://registry.npmjs.org/react-router cache-miss
138 http fetch GET 200 https://registry.npmjs.org/esbuild 444ms (cache miss)
139 silly packumentCache full:https://registry.npmjs.org/esbuild set size:undefined disposed:false
140 silly fetch manifest @remix-run/router@1.23.0
141 silly packumentCache full:https://registry.npmjs.org/@remix-run%2frouter cache-miss
142 http fetch GET 200 https://registry.npmjs.org/rollup 544ms (cache miss)
143 silly packumentCache full:https://registry.npmjs.org/rollup set size:undefined disposed:false
144 http fetch GET 200 https://registry.npmjs.org/@babel%2fplugin-transform-react-jsx-self 700ms (cache miss)
145 silly packumentCache full:https://registry.npmjs.org/@babel%2fplugin-transform-react-jsx-self set size:undefined disposed:false
146 http fetch GET 200 https://registry.npmjs.org/@babel%2fcore 704ms (cache miss)
147 silly packumentCache full:https://registry.npmjs.org/@babel%2fcore set size:undefined disposed:false
148 http fetch GET 200 https://registry.npmjs.org/@remix-run%2frouter 187ms (cache miss)
149 silly packumentCache full:https://registry.npmjs.org/@remix-run%2frouter set size:undefined disposed:false
150 http fetch GET 200 https://registry.npmjs.org/scheduler 860ms (cache miss)
151 silly packumentCache full:https://registry.npmjs.org/scheduler set size:undefined disposed:false
152 http fetch GET 200 https://registry.npmjs.org/react-router 1176ms (cache miss)
153 silly packumentCache full:https://registry.npmjs.org/react-router set size:undefined disposed:false
154 http fetch GET 200 https://registry.npmjs.org/react-refresh 1913ms (cache miss)
155 silly packumentCache full:https://registry.npmjs.org/react-refresh set size:undefined disposed:false
156 silly placeDep ROOT @types/prop-types@15.7.14 OK for: @types/react@18.3.21 want: *
157 silly placeDep ROOT csstype@3.1.3 OK for: @types/react@18.3.21 want: ^3.0.2
158 silly placeDep ROOT @babel/core@7.27.1 OK for: @vitejs/plugin-react@4.4.1 want: ^7.26.10
159 silly placeDep ROOT @babel/plugin-transform-react-jsx-self@7.27.1 OK for: @vitejs/plugin-react@4.4.1 want: ^7.25.9
160 silly placeDep ROOT @babel/plugin-transform-react-jsx-source@7.27.1 OK for: @vitejs/plugin-react@4.4.1 want: ^7.25.9
161 silly placeDep ROOT @types/babel__core@7.20.5 OK for: @vitejs/plugin-react@4.4.1 want: ^7.20.5
162 silly placeDep ROOT react-refresh@0.17.0 OK for: @vitejs/plugin-react@4.4.1 want: ^0.17.0
163 silly fetch manifest @ampproject/remapping@^2.2.0
164 silly packumentCache full:https://registry.npmjs.org/@ampproject%2fremapping cache-miss
165 silly fetch manifest @babel/code-frame@^7.27.1
166 silly packumentCache full:https://registry.npmjs.org/@babel%2fcode-frame cache-miss
167 silly fetch manifest @babel/generator@^7.27.1
168 silly packumentCache full:https://registry.npmjs.org/@babel%2fgenerator cache-miss
169 silly fetch manifest @babel/helper-compilation-targets@^7.27.1
170 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-compilation-targets cache-miss
171 silly fetch manifest @babel/helper-module-transforms@^7.27.1
172 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-module-transforms cache-miss
173 silly fetch manifest @babel/helpers@^7.27.1
174 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelpers cache-miss
175 silly fetch manifest @babel/parser@^7.27.1
176 silly packumentCache full:https://registry.npmjs.org/@babel%2fparser cache-miss
177 http fetch GET 200 https://registry.npmjs.org/@babel%2fgenerator 110ms (cache miss)
178 silly packumentCache full:https://registry.npmjs.org/@babel%2fgenerator set size:undefined disposed:false
179 silly fetch manifest @babel/template@^7.27.1
180 silly packumentCache full:https://registry.npmjs.org/@babel%2ftemplate cache-miss
181 http fetch GET 200 https://registry.npmjs.org/@ampproject%2fremapping 124ms (cache miss)
182 silly packumentCache full:https://registry.npmjs.org/@ampproject%2fremapping set size:undefined disposed:false
183 silly fetch manifest @babel/traverse@^7.27.1
184 silly packumentCache full:https://registry.npmjs.org/@babel%2ftraverse cache-miss
185 http fetch GET 200 https://registry.npmjs.org/@babel%2fcode-frame 133ms (cache miss)
186 silly packumentCache full:https://registry.npmjs.org/@babel%2fcode-frame set size:undefined disposed:false
187 silly fetch manifest @babel/types@^7.27.1
188 silly packumentCache full:https://registry.npmjs.org/@babel%2ftypes cache-miss
189 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelpers 137ms (cache miss)
190 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelpers set size:undefined disposed:false
191 silly fetch manifest convert-source-map@^2.0.0
192 silly packumentCache full:https://registry.npmjs.org/convert-source-map cache-miss
193 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-compilation-targets 140ms (cache miss)
194 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-compilation-targets set size:undefined disposed:false
195 silly fetch manifest debug@^4.1.0
196 silly packumentCache full:https://registry.npmjs.org/debug cache-miss
197 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-module-transforms 168ms (cache miss)
198 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-module-transforms set size:undefined disposed:false
199 silly fetch manifest gensync@^1.0.0-beta.2
200 silly packumentCache full:https://registry.npmjs.org/gensync cache-miss
201 http fetch GET 200 https://registry.npmjs.org/@babel%2fparser 172ms (cache miss)
202 silly packumentCache full:https://registry.npmjs.org/@babel%2fparser set size:undefined disposed:false
203 silly fetch manifest json5@^2.2.3
204 silly packumentCache full:https://registry.npmjs.org/json5 cache-miss
205 http fetch GET 200 https://registry.npmjs.org/convert-source-map 65ms (cache miss)
206 silly packumentCache full:https://registry.npmjs.org/convert-source-map set size:undefined disposed:false
207 silly fetch manifest semver@^6.3.1
208 silly packumentCache full:https://registry.npmjs.org/semver cache-miss
209 http fetch GET 200 https://registry.npmjs.org/debug 79ms (cache miss)
210 silly packumentCache full:https://registry.npmjs.org/debug set size:undefined disposed:false
211 silly fetch manifest @babel/helper-plugin-utils@^7.27.1
212 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-plugin-utils cache-miss
213 http fetch GET 200 https://registry.npmjs.org/@babel%2ftraverse 121ms (cache miss)
214 silly packumentCache full:https://registry.npmjs.org/@babel%2ftraverse set size:undefined disposed:false
215 silly fetch manifest @babel/helper-plugin-utils@^7.27.1
216 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-plugin-utils cache-miss
217 http fetch GET 200 https://registry.npmjs.org/gensync 85ms (cache miss)
218 silly packumentCache full:https://registry.npmjs.org/gensync set size:undefined disposed:false
219 silly fetch manifest @babel/types@^7.20.7
220 silly packumentCache full:https://registry.npmjs.org/@babel%2ftypes cache-miss
221 http fetch GET 200 https://registry.npmjs.org/@babel%2ftypes 136ms (cache miss)
222 silly packumentCache full:https://registry.npmjs.org/@babel%2ftypes set size:undefined disposed:false
223 silly fetch manifest @babel/parser@^7.20.7
224 silly packumentCache full:https://registry.npmjs.org/@babel%2fparser cache-miss
225 http fetch GET 200 https://registry.npmjs.org/semver 70ms (cache miss)
226 silly packumentCache full:https://registry.npmjs.org/semver set size:undefined disposed:false
227 silly fetch manifest @types/babel__template@*
228 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__template cache-miss
229 http cache https://registry.npmjs.org/@babel%2fparser 8ms (cache hit)
230 silly packumentCache full:https://registry.npmjs.org/@babel%2fparser set size:676433 disposed:false
231 silly fetch manifest @types/babel__traverse@*
232 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__traverse cache-miss
233 http fetch GET 200 https://registry.npmjs.org/json5 107ms (cache miss)
234 silly packumentCache full:https://registry.npmjs.org/json5 set size:undefined disposed:false
235 silly fetch manifest @types/babel__generator@*
236 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__generator cache-miss
237 http fetch GET 200 https://registry.npmjs.org/@babel%2ftemplate 173ms (cache miss)
238 silly packumentCache full:https://registry.npmjs.org/@babel%2ftemplate set size:undefined disposed:false
239 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-plugin-utils 88ms (cache miss)
240 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-plugin-utils set size:undefined disposed:false
241 http fetch GET 200 https://registry.npmjs.org/@types%2fbabel__template 85ms (cache miss)
242 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__template set size:undefined disposed:false
243 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-plugin-utils 111ms (cache miss)
244 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-plugin-utils set size:undefined disposed:false
245 http fetch GET 200 https://registry.npmjs.org/@types%2fbabel__generator 84ms (cache miss)
246 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__generator set size:undefined disposed:false
247 http fetch GET 200 https://registry.npmjs.org/@babel%2ftypes 128ms (cache miss)
248 silly packumentCache full:https://registry.npmjs.org/@babel%2ftypes set size:undefined disposed:false
249 http fetch GET 200 https://registry.npmjs.org/@types%2fbabel__traverse 127ms (cache miss)
250 silly packumentCache full:https://registry.npmjs.org/@types%2fbabel__traverse set size:undefined disposed:false
251 silly fetch manifest @babel/core@^7.0.0
252 silly packumentCache full:https://registry.npmjs.org/@babel%2fcore cache-miss
253 http cache https://registry.npmjs.org/@babel%2fcore 4ms (cache hit)
254 silly packumentCache full:https://registry.npmjs.org/@babel%2fcore set size:702395 disposed:false
255 silly placeDep ROOT @ampproject/remapping@2.3.0 OK for: @babel/core@7.27.1 want: ^2.2.0
256 silly placeDep ROOT @babel/code-frame@7.27.1 OK for: @babel/core@7.27.1 want: ^7.27.1
257 silly placeDep ROOT @babel/generator@7.27.1 OK for: @babel/core@7.27.1 want: ^7.27.1
258 silly placeDep ROOT @babel/helper-compilation-targets@7.27.2 OK for: @babel/core@7.27.1 want: ^7.27.1
259 silly placeDep ROOT @babel/helper-module-transforms@7.27.1 OK for: @babel/core@7.27.1 want: ^7.27.1
260 silly placeDep ROOT @babel/helpers@7.27.1 OK for: @babel/core@7.27.1 want: ^7.27.1
261 silly placeDep ROOT @babel/parser@7.27.2 OK for: @babel/core@7.27.1 want: ^7.27.1
262 silly placeDep ROOT @babel/template@7.27.2 OK for: @babel/core@7.27.1 want: ^7.27.1
263 silly placeDep ROOT @babel/traverse@7.27.1 OK for: @babel/core@7.27.1 want: ^7.27.1
264 silly placeDep ROOT @babel/types@7.27.1 OK for: @babel/core@7.27.1 want: ^7.27.1
265 silly placeDep ROOT convert-source-map@2.0.0 OK for: @babel/core@7.27.1 want: ^2.0.0
266 silly placeDep ROOT debug@4.4.0 OK for: @babel/core@7.27.1 want: ^4.1.0
267 silly placeDep ROOT gensync@1.0.0-beta.2 OK for: @babel/core@7.27.1 want: ^1.0.0-beta.2
268 silly placeDep ROOT json5@2.2.3 OK for: @babel/core@7.27.1 want: ^2.2.3
269 silly placeDep ROOT semver@6.3.1 OK for: @babel/core@7.27.1 want: ^6.3.1
270 silly fetch manifest @jridgewell/gen-mapping@^0.3.5
271 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fgen-mapping cache-miss
272 silly fetch manifest @jridgewell/trace-mapping@^0.3.24
273 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2ftrace-mapping cache-miss
274 silly fetch manifest @babel/helper-validator-identifier@^7.27.1
275 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-validator-identifier cache-miss
276 silly fetch manifest js-tokens@^4.0.0
277 silly packumentCache full:https://registry.npmjs.org/js-tokens cache-miss
278 silly fetch manifest picocolors@^1.1.1
279 silly packumentCache full:https://registry.npmjs.org/picocolors cache-miss
280 silly fetch manifest @jridgewell/gen-mapping@^0.3.5
281 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fgen-mapping cache-miss
282 silly fetch manifest @jridgewell/trace-mapping@^0.3.25
283 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2ftrace-mapping cache-miss
284 http fetch GET 200 https://registry.npmjs.org/picocolors 67ms (cache miss)
285 silly packumentCache full:https://registry.npmjs.org/picocolors set size:undefined disposed:false
286 silly fetch manifest jsesc@^3.0.2
287 silly packumentCache full:https://registry.npmjs.org/jsesc cache-miss
288 http fetch GET 200 https://registry.npmjs.org/js-tokens 71ms (cache miss)
289 silly packumentCache full:https://registry.npmjs.org/js-tokens set size:undefined disposed:false
290 silly fetch manifest @babel/compat-data@^7.27.2
291 silly packumentCache full:https://registry.npmjs.org/@babel%2fcompat-data cache-miss
292 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2ftrace-mapping 82ms (cache miss)
293 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2ftrace-mapping set size:undefined disposed:false
294 silly fetch manifest @babel/helper-validator-option@^7.27.1
295 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-validator-option cache-miss
296 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2fgen-mapping 103ms (cache miss)
297 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fgen-mapping set size:undefined disposed:false
298 silly fetch manifest browserslist@^4.24.0
299 silly packumentCache full:https://registry.npmjs.org/browserslist cache-miss
300 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2fgen-mapping 105ms (cache miss)
301 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fgen-mapping set size:undefined disposed:false
302 silly fetch manifest lru-cache@^5.1.1
303 silly packumentCache full:https://registry.npmjs.org/lru-cache cache-miss
304 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-validator-identifier 107ms (cache miss)
305 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-validator-identifier set size:undefined disposed:false
306 silly fetch manifest @babel/helper-module-imports@^7.27.1
307 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-module-imports cache-miss
308 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2ftrace-mapping 109ms (cache miss)
309 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2ftrace-mapping set size:undefined disposed:false
310 silly fetch manifest debug@^4.3.1
311 silly packumentCache full:https://registry.npmjs.org/debug cache-miss
312 http cache https://registry.npmjs.org/debug 2ms (cache hit)
313 silly packumentCache full:https://registry.npmjs.org/debug set size:191237 disposed:false
314 silly fetch manifest globals@^11.1.0
315 silly packumentCache full:https://registry.npmjs.org/globals cache-miss
316 http fetch GET 200 https://registry.npmjs.org/jsesc 72ms (cache miss)
317 silly packumentCache full:https://registry.npmjs.org/jsesc set size:undefined disposed:false
318 silly fetch manifest @babel/helper-string-parser@^7.27.1
319 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-string-parser cache-miss
320 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-validator-option 70ms (cache miss)
321 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-validator-option set size:undefined disposed:false
322 silly fetch manifest ms@^2.1.3
323 silly packumentCache full:https://registry.npmjs.org/ms cache-miss
324 http fetch GET 200 https://registry.npmjs.org/@babel%2fcompat-data 92ms (cache miss)
325 silly packumentCache full:https://registry.npmjs.org/@babel%2fcompat-data set size:undefined disposed:false
326 http fetch GET 200 https://registry.npmjs.org/browserslist 94ms (cache miss)
327 silly packumentCache full:https://registry.npmjs.org/browserslist set size:undefined disposed:false
328 http fetch GET 200 https://registry.npmjs.org/globals 101ms (cache miss)
329 silly packumentCache full:https://registry.npmjs.org/globals set size:undefined disposed:false
330 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-module-imports 112ms (cache miss)
331 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-module-imports set size:undefined disposed:false
332 http fetch GET 200 https://registry.npmjs.org/ms 75ms (cache miss)
333 silly packumentCache full:https://registry.npmjs.org/ms set size:undefined disposed:false
334 http fetch GET 200 https://registry.npmjs.org/lru-cache 124ms (cache miss)
335 silly packumentCache full:https://registry.npmjs.org/lru-cache set size:undefined disposed:false
336 http fetch GET 200 https://registry.npmjs.org/@babel%2fhelper-string-parser 94ms (cache miss)
337 silly packumentCache full:https://registry.npmjs.org/@babel%2fhelper-string-parser set size:undefined disposed:false
338 silly placeDep ROOT @jridgewell/gen-mapping@0.3.8 OK for: @ampproject/remapping@2.3.0 want: ^0.3.5
339 silly placeDep ROOT @jridgewell/trace-mapping@0.3.25 OK for: @ampproject/remapping@2.3.0 want: ^0.3.24
340 silly fetch manifest @jridgewell/set-array@^1.2.1
341 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fset-array cache-miss
342 silly fetch manifest @jridgewell/sourcemap-codec@^1.4.10
343 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fsourcemap-codec cache-miss
344 silly fetch manifest @jridgewell/resolve-uri@^3.1.0
345 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fresolve-uri cache-miss
346 silly fetch manifest @jridgewell/sourcemap-codec@^1.4.14
347 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fsourcemap-codec cache-miss
348 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2fset-array 75ms (cache miss)
349 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fset-array set size:undefined disposed:false
350 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2fresolve-uri 107ms (cache miss)
351 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fresolve-uri set size:undefined disposed:false
352 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2fsourcemap-codec 118ms (cache miss)
353 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fsourcemap-codec set size:undefined disposed:false
354 http fetch GET 200 https://registry.npmjs.org/@jridgewell%2fsourcemap-codec 121ms (cache miss)
355 silly packumentCache full:https://registry.npmjs.org/@jridgewell%2fsourcemap-codec set size:undefined disposed:false
356 silly placeDep ROOT @babel/helper-validator-identifier@7.27.1 OK for: @babel/code-frame@7.27.1 want: ^7.27.1
357 silly placeDep ROOT js-tokens@4.0.0 OK for: @babel/code-frame@7.27.1 want: ^4.0.0
358 silly placeDep ROOT picocolors@1.1.1 OK for: @babel/code-frame@7.27.1 want: ^1.1.1
359 silly placeDep ROOT jsesc@3.1.0 OK for: @babel/generator@7.27.1 want: ^3.0.2
360 silly placeDep ROOT @babel/compat-data@7.27.2 OK for: @babel/helper-compilation-targets@7.27.2 want: ^7.27.2
361 silly placeDep ROOT @babel/helper-validator-option@7.27.1 OK for: @babel/helper-compilation-targets@7.27.2 want: ^7.27.1
362 silly placeDep ROOT browserslist@4.24.5 OK for: @babel/helper-compilation-targets@7.27.2 want: ^4.24.0
363 silly placeDep ROOT lru-cache@5.1.1 OK for: @babel/helper-compilation-targets@7.27.2 want: ^5.1.1
364 silly fetch manifest caniuse-lite@^1.0.30001716
365 silly packumentCache full:https://registry.npmjs.org/caniuse-lite cache-miss
366 silly fetch manifest electron-to-chromium@^1.5.149
367 silly packumentCache full:https://registry.npmjs.org/electron-to-chromium cache-miss
368 silly fetch manifest node-releases@^2.0.19
369 silly packumentCache full:https://registry.npmjs.org/node-releases cache-miss
370 silly fetch manifest update-browserslist-db@^1.1.3
371 silly packumentCache full:https://registry.npmjs.org/update-browserslist-db cache-miss
372 silly fetch manifest yallist@^3.0.2
373 silly packumentCache full:https://registry.npmjs.org/yallist cache-miss
374 http fetch GET 200 https://registry.npmjs.org/update-browserslist-db 71ms (cache miss)
375 silly packumentCache full:https://registry.npmjs.org/update-browserslist-db set size:undefined disposed:false
376 http fetch GET 200 https://registry.npmjs.org/yallist 84ms (cache miss)
377 silly packumentCache full:https://registry.npmjs.org/yallist set size:undefined disposed:false
378 http fetch GET 200 https://registry.npmjs.org/node-releases 159ms (cache miss)
379 silly packumentCache full:https://registry.npmjs.org/node-releases set size:undefined disposed:false
380 http fetch GET 200 https://registry.npmjs.org/caniuse-lite 288ms (cache miss)
381 silly packumentCache full:https://registry.npmjs.org/caniuse-lite set size:undefined disposed:false
382 http fetch GET 200 https://registry.npmjs.org/electron-to-chromium 620ms (cache miss)
383 silly packumentCache full:https://registry.npmjs.org/electron-to-chromium set size:undefined disposed:false
384 silly placeDep ROOT @babel/helper-module-imports@7.27.1 OK for: @babel/helper-module-transforms@7.27.1 want: ^7.27.1
385 silly placeDep ROOT @babel/helper-plugin-utils@7.27.1 OK for: @babel/plugin-transform-react-jsx-self@7.27.1 want: ^7.27.1
386 silly placeDep ROOT globals@11.12.0 OK for: @babel/traverse@7.27.1 want: ^11.1.0
387 silly placeDep ROOT @babel/helper-string-parser@7.27.1 OK for: @babel/types@7.27.1 want: ^7.27.1
388 silly placeDep ROOT @jridgewell/set-array@1.2.1 OK for: @jridgewell/gen-mapping@0.3.8 want: ^1.2.1
389 silly placeDep ROOT @jridgewell/sourcemap-codec@1.5.0 OK for: @jridgewell/gen-mapping@0.3.8 want: ^1.4.10
390 silly placeDep ROOT @jridgewell/resolve-uri@3.1.2 OK for: @jridgewell/trace-mapping@0.3.25 want: ^3.1.0
391 silly placeDep ROOT @types/babel__generator@7.27.0 OK for: @types/babel__core@7.20.5 want: *
392 silly placeDep ROOT @types/babel__template@7.4.4 OK for: @types/babel__core@7.20.5 want: *
393 silly placeDep ROOT @types/babel__traverse@7.20.7 OK for: @types/babel__core@7.20.5 want: *
394 silly fetch manifest browserslist@>= 4.21.0
395 silly packumentCache full:https://registry.npmjs.org/browserslist cache-miss
396 http cache https://registry.npmjs.org/browserslist 10ms (cache hit)
397 silly packumentCache full:https://registry.npmjs.org/browserslist set size:478931 disposed:false
398 silly placeDep ROOT caniuse-lite@1.0.30001717 OK for: browserslist@4.24.5 want: ^1.0.30001716
399 silly placeDep ROOT electron-to-chromium@1.5.151 OK for: browserslist@4.24.5 want: ^1.5.149
400 silly placeDep ROOT node-releases@2.0.19 OK for: browserslist@4.24.5 want: ^2.0.19
401 silly placeDep ROOT update-browserslist-db@1.1.3 OK for: browserslist@4.24.5 want: ^1.1.3
402 silly fetch manifest escalade@^3.2.0
403 silly packumentCache full:https://registry.npmjs.org/escalade cache-miss
404 http fetch GET 200 https://registry.npmjs.org/escalade 87ms (cache miss)
405 silly packumentCache full:https://registry.npmjs.org/escalade set size:undefined disposed:false
406 silly placeDep ROOT ms@2.1.3 OK for: debug@4.4.0 want: ^2.1.3
407 silly placeDep ROOT yallist@3.1.1 OK for: lru-cache@5.1.1 want: ^3.0.2
408 silly placeDep ROOT loose-envify@1.4.0 OK for: react@18.3.1 want: ^1.1.0
409 silly placeDep ROOT scheduler@0.23.2 OK for: react-dom@18.3.1 want: ^0.23.2
410 silly fetch manifest react@>=16.8
411 silly packumentCache full:https://registry.npmjs.org/react cache-miss
412 http cache https://registry.npmjs.org/react 15ms (cache hit)
413 silly packumentCache full:https://registry.npmjs.org/react set size:5677276 disposed:false
414 silly placeDep ROOT @remix-run/router@1.23.0 OK for: react-router-dom@6.30.0 want: 1.23.0
415 silly placeDep ROOT react-router@6.30.0 OK for: react-router-dom@6.30.0 want: 6.30.0
416 silly placeDep ROOT escalade@3.2.0 OK for: update-browserslist-db@1.1.3 want: ^3.2.0
417 silly placeDep ROOT esbuild@0.21.5 OK for: vite@5.4.19 want: ^0.21.3
418 silly placeDep ROOT fsevents@2.3.3 OK for: vite@5.4.19 want: ~2.3.3
419 silly placeDep ROOT postcss@8.5.3 OK for: vite@5.4.19 want: ^8.4.43
420 silly placeDep ROOT rollup@4.40.2 OK for: vite@5.4.19 want: ^4.20.0
421 silly fetch manifest @esbuild/aix-ppc64@0.21.5
422 silly packumentCache full:https://registry.npmjs.org/@esbuild%2faix-ppc64 cache-miss
423 silly fetch manifest @esbuild/linux-arm@0.21.5
424 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-arm cache-miss
425 silly fetch manifest @esbuild/linux-x64@0.21.5
426 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-x64 cache-miss
427 silly fetch manifest @esbuild/sunos-x64@0.21.5
428 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fsunos-x64 cache-miss
429 silly fetch manifest @esbuild/win32-x64@0.21.5
430 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fwin32-x64 cache-miss
431 silly fetch manifest @esbuild/darwin-x64@0.21.5
432 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fdarwin-x64 cache-miss
433 silly fetch manifest @esbuild/linux-ia32@0.21.5
434 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-ia32 cache-miss
435 http fetch GET 200 https://registry.npmjs.org/@esbuild%2faix-ppc64 82ms (cache miss)
436 silly packumentCache full:https://registry.npmjs.org/@esbuild%2faix-ppc64 set size:undefined disposed:false
437 silly fetch manifest @esbuild/netbsd-x64@0.21.5
438 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fnetbsd-x64 cache-miss
439 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fwin32-x64 95ms (cache miss)
440 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fwin32-x64 set size:undefined disposed:false
441 silly fetch manifest @esbuild/win32-ia32@0.21.5
442 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fwin32-ia32 cache-miss
443 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-x64 99ms (cache miss)
444 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-x64 set size:undefined disposed:false
445 silly fetch manifest @esbuild/android-arm@0.21.5
446 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fandroid-arm cache-miss
447 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-ia32 112ms (cache miss)
448 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-ia32 set size:undefined disposed:false
449 silly fetch manifest @esbuild/android-x64@0.21.5
450 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fandroid-x64 cache-miss
451 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-arm 118ms (cache miss)
452 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-arm set size:undefined disposed:false
453 silly fetch manifest @esbuild/freebsd-x64@0.21.5
454 silly packumentCache full:https://registry.npmjs.org/@esbuild%2ffreebsd-x64 cache-miss
455 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fsunos-x64 122ms (cache miss)
456 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fsunos-x64 set size:undefined disposed:false
457 silly fetch manifest @esbuild/linux-arm64@0.21.5
458 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-arm64 cache-miss
459 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fdarwin-x64 147ms (cache miss)
460 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fdarwin-x64 set size:undefined disposed:false
461 silly fetch manifest @esbuild/linux-ppc64@0.21.5
462 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-ppc64 cache-miss
463 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fwin32-ia32 104ms (cache miss)
464 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fwin32-ia32 set size:undefined disposed:false
465 silly fetch manifest @esbuild/linux-s390x@0.21.5
466 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-s390x cache-miss
467 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fandroid-arm 107ms (cache miss)
468 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fandroid-arm set size:undefined disposed:false
469 silly fetch manifest @esbuild/openbsd-x64@0.21.5
470 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fopenbsd-x64 cache-miss
471 http fetch GET 200 https://registry.npmjs.org/@esbuild%2ffreebsd-x64 101ms (cache miss)
472 silly packumentCache full:https://registry.npmjs.org/@esbuild%2ffreebsd-x64 set size:undefined disposed:false
473 silly fetch manifest @esbuild/win32-arm64@0.21.5
474 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fwin32-arm64 cache-miss
475 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fnetbsd-x64 146ms (cache miss)
476 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fnetbsd-x64 set size:undefined disposed:false
477 silly fetch manifest @esbuild/darwin-arm64@0.21.5
478 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fdarwin-arm64 cache-miss
479 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fandroid-x64 118ms (cache miss)
480 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fandroid-x64 set size:undefined disposed:false
481 silly fetch manifest @esbuild/android-arm64@0.21.5
482 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fandroid-arm64 cache-miss
483 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-arm64 135ms (cache miss)
484 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-arm64 set size:undefined disposed:false
485 silly fetch manifest @esbuild/freebsd-arm64@0.21.5
486 silly packumentCache full:https://registry.npmjs.org/@esbuild%2ffreebsd-arm64 cache-miss
487 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-ppc64 123ms (cache miss)
488 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-ppc64 set size:undefined disposed:false
489 silly fetch manifest @esbuild/linux-loong64@0.21.5
490 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-loong64 cache-miss
491 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-s390x 98ms (cache miss)
492 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-s390x set size:undefined disposed:false
493 silly fetch manifest @esbuild/linux-riscv64@0.21.5
494 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-riscv64 cache-miss
495 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fopenbsd-x64 109ms (cache miss)
496 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fopenbsd-x64 set size:undefined disposed:false
497 silly fetch manifest @esbuild/linux-mips64el@0.21.5
498 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-mips64el cache-miss
499 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fwin32-arm64 102ms (cache miss)
500 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fwin32-arm64 set size:undefined disposed:false
501 silly fetch manifest nanoid@^3.3.8
502 silly packumentCache full:https://registry.npmjs.org/nanoid cache-miss
503 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fdarwin-arm64 99ms (cache miss)
504 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fdarwin-arm64 set size:undefined disposed:false
505 silly fetch manifest source-map-js@^1.2.1
506 silly packumentCache full:https://registry.npmjs.org/source-map-js cache-miss
507 http fetch GET 200 https://registry.npmjs.org/@esbuild%2fandroid-arm64 105ms (cache miss)
508 silly packumentCache full:https://registry.npmjs.org/@esbuild%2fandroid-arm64 set size:undefined disposed:false
509 silly fetch manifest @types/estree@1.0.7
510 silly packumentCache full:https://registry.npmjs.org/@types%2festree cache-miss
511 http fetch GET 200 https://registry.npmjs.org/@esbuild%2ffreebsd-arm64 152ms (cache miss)
512 silly packumentCache full:https://registry.npmjs.org/@esbuild%2ffreebsd-arm64 set size:undefined disposed:false
513 silly fetch manifest @rollup/rollup-darwin-arm64@4.40.2
514 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-darwin-arm64 cache-miss
515 http fetch GET 200 https://registry.npmjs.org/nanoid 91ms (cache miss)
516 silly packumentCache full:https://registry.npmjs.org/nanoid set size:undefined disposed:false
517 silly fetch manifest @rollup/rollup-android-arm64@4.40.2
518 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-android-arm64 cache-miss
519 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-riscv64 118ms (cache miss)
520 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-riscv64 set size:undefined disposed:false
521 silly fetch manifest @rollup/rollup-win32-arm64-msvc@4.40.2
522 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-win32-arm64-msvc cache-miss
523 http fetch GET 200 https://registry.npmjs.org/source-map-js 92ms (cache miss)
524 silly packumentCache full:https://registry.npmjs.org/source-map-js set size:undefined disposed:false
525 silly fetch manifest @rollup/rollup-freebsd-arm64@4.40.2
526 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-freebsd-arm64 cache-miss
527 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-loong64 152ms (cache miss)
528 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-loong64 set size:undefined disposed:false
529 silly fetch manifest @rollup/rollup-linux-arm64-gnu@4.40.2
530 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm64-gnu cache-miss
531 http fetch GET 200 https://registry.npmjs.org/@esbuild%2flinux-mips64el 112ms (cache miss)
532 silly packumentCache full:https://registry.npmjs.org/@esbuild%2flinux-mips64el set size:undefined disposed:false
533 silly fetch manifest @rollup/rollup-linux-arm64-musl@4.40.2
534 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm64-musl cache-miss
535 http fetch GET 200 https://registry.npmjs.org/@types%2festree 99ms (cache miss)
536 silly packumentCache full:https://registry.npmjs.org/@types%2festree set size:undefined disposed:false
537 silly fetch manifest @rollup/rollup-android-arm-eabi@4.40.2
538 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-android-arm-eabi cache-miss
539 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-win32-arm64-msvc 84ms (cache miss)
540 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-win32-arm64-msvc set size:undefined disposed:false
541 silly fetch manifest @rollup/rollup-linux-arm-gnueabihf@4.40.2
542 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm-gnueabihf cache-miss
543 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-android-arm64 94ms (cache miss)
544 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-android-arm64 set size:undefined disposed:false
545 silly fetch manifest @rollup/rollup-linux-arm-musleabihf@4.40.2
546 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm-musleabihf cache-miss
547 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-android-arm-eabi 89ms (cache miss)
548 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-android-arm-eabi set size:undefined disposed:false
549 silly fetch manifest @rollup/rollup-win32-ia32-msvc@4.40.2
550 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-win32-ia32-msvc cache-miss
551 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-freebsd-arm64 107ms (cache miss)
552 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-freebsd-arm64 set size:undefined disposed:false
553 silly fetch manifest @rollup/rollup-linux-loongarch64-gnu@4.40.2
554 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-loongarch64-gnu cache-miss
555 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-arm64-musl 98ms (cache miss)
556 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm64-musl set size:undefined disposed:false
557 silly fetch manifest @rollup/rollup-linux-riscv64-gnu@4.40.2
558 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-riscv64-gnu cache-miss
559 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-arm64-gnu 127ms (cache miss)
560 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm64-gnu set size:undefined disposed:false
561 silly fetch manifest @rollup/rollup-linux-riscv64-musl@4.40.2
562 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-riscv64-musl cache-miss
563 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-darwin-arm64 164ms (cache miss)
564 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-darwin-arm64 set size:undefined disposed:false
565 silly fetch manifest @rollup/rollup-linux-powerpc64le-gnu@4.40.2
566 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-powerpc64le-gnu cache-miss
567 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-arm-musleabihf 88ms (cache miss)
568 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm-musleabihf set size:undefined disposed:false
569 silly fetch manifest @rollup/rollup-linux-s390x-gnu@4.40.2
570 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-s390x-gnu cache-miss
571 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-win32-ia32-msvc 94ms (cache miss)
572 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-win32-ia32-msvc set size:undefined disposed:false
573 silly fetch manifest @rollup/rollup-darwin-x64@4.40.2
574 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-darwin-x64 cache-miss
575 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-riscv64-gnu 98ms (cache miss)
576 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-riscv64-gnu set size:undefined disposed:false
577 silly fetch manifest @rollup/rollup-win32-x64-msvc@4.40.2
578 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-win32-x64-msvc cache-miss
579 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-loongarch64-gnu 106ms (cache miss)
580 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-loongarch64-gnu set size:undefined disposed:false
581 silly fetch manifest @rollup/rollup-freebsd-x64@4.40.2
582 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-freebsd-x64 cache-miss
583 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-riscv64-musl 99ms (cache miss)
584 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-riscv64-musl set size:undefined disposed:false
585 silly fetch manifest @rollup/rollup-linux-x64-gnu@4.40.2
586 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-x64-gnu cache-miss
587 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-arm-gnueabihf 179ms (cache miss)
588 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-arm-gnueabihf set size:undefined disposed:false
589 silly fetch manifest @rollup/rollup-linux-x64-musl@4.40.2
590 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-x64-musl cache-miss
591 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-darwin-x64 90ms (cache miss)
592 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-darwin-x64 set size:undefined disposed:false
593 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-s390x-gnu 127ms (cache miss)
594 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-s390x-gnu set size:undefined disposed:false
595 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-freebsd-x64 94ms (cache miss)
596 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-freebsd-x64 set size:undefined disposed:false
597 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-win32-x64-msvc 102ms (cache miss)
598 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-win32-x64-msvc set size:undefined disposed:false
599 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-x64-gnu 101ms (cache miss)
600 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-x64-gnu set size:undefined disposed:false
601 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-x64-musl 97ms (cache miss)
602 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-x64-musl set size:undefined disposed:false
603 http fetch GET 200 https://registry.npmjs.org/@rollup%2frollup-linux-powerpc64le-gnu 208ms (cache miss)
604 silly packumentCache full:https://registry.npmjs.org/@rollup%2frollup-linux-powerpc64le-gnu set size:undefined disposed:false
605 silly placeDep ROOT @esbuild/aix-ppc64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
606 silly placeDep ROOT @esbuild/android-arm@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
607 silly placeDep ROOT @esbuild/android-arm64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
608 silly placeDep ROOT @esbuild/android-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
609 silly placeDep ROOT @esbuild/darwin-arm64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
610 silly placeDep ROOT @esbuild/darwin-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
611 silly placeDep ROOT @esbuild/freebsd-arm64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
612 silly placeDep ROOT @esbuild/freebsd-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
613 silly placeDep ROOT @esbuild/linux-arm@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
614 silly placeDep ROOT @esbuild/linux-arm64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
615 silly placeDep ROOT @esbuild/linux-ia32@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
616 silly placeDep ROOT @esbuild/linux-loong64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
617 silly placeDep ROOT @esbuild/linux-mips64el@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
618 silly placeDep ROOT @esbuild/linux-ppc64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
619 silly placeDep ROOT @esbuild/linux-riscv64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
620 silly placeDep ROOT @esbuild/linux-s390x@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
621 silly placeDep ROOT @esbuild/linux-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
622 silly placeDep ROOT @esbuild/netbsd-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
623 silly placeDep ROOT @esbuild/openbsd-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
624 silly placeDep ROOT @esbuild/sunos-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
625 silly placeDep ROOT @esbuild/win32-arm64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
626 silly placeDep ROOT @esbuild/win32-ia32@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
627 silly placeDep ROOT @esbuild/win32-x64@0.21.5 OK for: esbuild@0.21.5 want: 0.21.5
628 silly placeDep ROOT nanoid@3.3.11 OK for: postcss@8.5.3 want: ^3.3.8
629 silly placeDep ROOT source-map-js@1.2.1 OK for: postcss@8.5.3 want: ^1.2.1
630 silly placeDep ROOT @rollup/rollup-android-arm-eabi@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
631 silly placeDep ROOT @rollup/rollup-android-arm64@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
632 silly placeDep ROOT @rollup/rollup-darwin-arm64@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
633 silly placeDep ROOT @rollup/rollup-darwin-x64@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
634 silly placeDep ROOT @rollup/rollup-freebsd-arm64@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
635 silly placeDep ROOT @rollup/rollup-freebsd-x64@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
636 silly placeDep ROOT @rollup/rollup-linux-arm-gnueabihf@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
637 silly placeDep ROOT @rollup/rollup-linux-arm-musleabihf@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
638 silly placeDep ROOT @rollup/rollup-linux-arm64-gnu@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
639 silly placeDep ROOT @rollup/rollup-linux-arm64-musl@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
640 silly placeDep ROOT @rollup/rollup-linux-loongarch64-gnu@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
641 silly placeDep ROOT @rollup/rollup-linux-powerpc64le-gnu@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
642 silly placeDep ROOT @rollup/rollup-linux-riscv64-gnu@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
643 silly placeDep ROOT @rollup/rollup-linux-riscv64-musl@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
644 silly placeDep ROOT @rollup/rollup-linux-s390x-gnu@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
645 silly placeDep ROOT @rollup/rollup-linux-x64-gnu@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
646 silly placeDep ROOT @rollup/rollup-linux-x64-musl@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
647 silly placeDep ROOT @rollup/rollup-win32-arm64-msvc@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
648 silly placeDep ROOT @rollup/rollup-win32-ia32-msvc@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
649 silly placeDep ROOT @rollup/rollup-win32-x64-msvc@4.40.2 OK for: rollup@4.40.2 want: 4.40.2
650 silly placeDep ROOT @types/estree@1.0.7 OK for: rollup@4.40.2 want: 1.0.7
651 verbose type range
652 verbose stack @types/react-router-dom: No matching version found for @types/react-router-dom@^6.23.1.
652 verbose stack     at module.exports (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/node_modules/npm-pick-manifest/lib/index.js:215:23)
652 verbose stack     at RegistryFetcher.manifest (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/node_modules/pacote/lib/registry.js:130:54)
652 verbose stack     at async #fetchManifest (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/node_modules/@npmcli/arborist/lib/arborist/build-ideal-tree.js:1202:20)
652 verbose stack     at async #nodeFromEdge (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/node_modules/@npmcli/arborist/lib/arborist/build-ideal-tree.js:1040:19)
652 verbose stack     at async #buildDepStep (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/node_modules/@npmcli/arborist/lib/arborist/build-ideal-tree.js:904:11)
652 verbose stack     at async Arborist.buildIdealTree (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/node_modules/@npmcli/arborist/lib/arborist/build-ideal-tree.js:181:7)
652 verbose stack     at async Promise.all (index 1)
652 verbose stack     at async Arborist.reify (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/node_modules/@npmcli/arborist/lib/arborist/reify.js:131:5)
652 verbose stack     at async Install.exec (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/lib/commands/install.js:150:5)
652 verbose stack     at async Npm.exec (/Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm/lib/npm.js:207:9)
653 error code ETARGET
654 error notarget No matching version found for @types/react-router-dom@^6.23.1.
655 error notarget In most cases you or one of your dependencies are requesting
655 error notarget a package version that doesn't exist.
656 silly unfinished npm timer reify 1746724930503
657 silly unfinished npm timer reify:loadTrees 1746724930503
658 verbose cwd /Users/nicholasjenkins/Documents/personalvibe/storymaker_spa
659 verbose os Darwin 24.2.0
660 verbose node v22.15.0
661 verbose npm  v10.9.2
662 notice
662 notice New [31mmajor[39m version of npm available! [31m10.9.2[39m -> [34m11.3.0[39m
662 notice Changelog: [34mhttps://github.com/npm/cli/releases/tag/v11.3.0[39m
662 notice To update run: [4mnpm install -g npm@11.3.0[24m
662 notice  { force: true, [Symbol(proc-log.meta)]: true }
663 verbose exit 1
664 verbose code 1
665 error A complete log of this run can be found in: /Users/nicholasjenkins/.npm/_logs/2025-05-08T17_22_10_203Z-debug-0.log
