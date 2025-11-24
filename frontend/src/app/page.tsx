'use client'

import { useState } from 'react'
import { 
  Upload, 
  Sparkles, 
  Search, 
  TrendingUp, 
  Cpu, 
  CheckCircle2, 
  ArrowRight, 
  ScanLine
} from 'lucide-react'
import { analyzeOutfit } from './actions'

interface VisualAnalysis {
  gender_style: string
  cut: string
  color: string
  fabric: string
  occasion: string
}

interface AnalysisResult {
  visual_analysis: VisualAnalysis
  trend_summary: string
  final_report: string
  generated_image_url: string
  analysis_mode: string
  generation_prompt: string
  image_generation_error: string | null
}

const AGENT_STEPS = [
  { id: 1, agent: "Vision Agent", action: "Analyzing outfit composition & colors...", icon: ScanLine },
  { id: 2, agent: "Trends Agent", action: "Scanning global fashion trends...", icon: TrendingUp },
  { id: 3, agent: "Advisor Agent", action: "Synthesizing styling recommendations...", icon: Cpu },
  { id: 4, agent: "Generator Agent", action: "Creating upgraded visualization...", icon: Sparkles },
]

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [query, setQuery] = useState('')
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [currentStep, setCurrentStep] = useState(0)
  const [view, setView] = useState<'upload' | 'processing' | 'results'>('upload')

  const handleAnalyze = async (mode: 'quick' | 'deep') => {
    if (!file) return

    setView('processing')
    setCurrentStep(0)
    setError(null)
    setAnalysis(null)

    // Simulate agent workflow
    let step = 0
    const stepInterval = setInterval(() => {
      step++
      setCurrentStep(step)
      if (step >= AGENT_STEPS.length) {
        clearInterval(stepInterval)
      }
    }, 1800)

    const formData = new FormData()
    formData.append('image', file)
    formData.append('query', query)
    formData.append('mode', mode)

    try {
      const result = await analyzeOutfit(formData)
      clearInterval(stepInterval)
      
      if (result.error) {
        setError(result.error)
        setView('upload')
      } else {
        setAnalysis(result)
        setTimeout(() => setView('results'), 800)
      }
    } catch {
      clearInterval(stepInterval)
      setError("An unexpected error occurred.")
      setView('upload')
    }
  }

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    setPreview(URL.createObjectURL(selectedFile))
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files?.[0]
    if (droppedFile && droppedFile.type.startsWith('image/')) {
      handleFileSelect(droppedFile)
    }
  }

  const handleReset = () => {
    setView('upload')
    setAnalysis(null)
    setError(null)
    setCurrentStep(0)
  }

  if (view === 'processing') {
    return (
      <div className="fixed inset-0 bg-white z-40 flex flex-col items-center justify-center p-8 animate-in fade-in duration-500">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center space-y-2">
            <div className="inline-block p-3 rounded-full bg-stone-50 border border-stone-200 mb-4 shadow-sm">
              <Cpu className="w-8 h-8 text-zinc-900 animate-pulse" />
            </div>
            <h2 className="font-serif text-3xl text-zinc-900">Orchestrating Look</h2>
            <p className="text-stone-500 font-light">The Supervisor Agent is coordinating your style team.</p>
          </div>

          <div className="space-y-4 relative">
            <div className="absolute left-[1.35rem] top-4 bottom-4 w-0.5 bg-stone-100 -z-10"></div>

            {AGENT_STEPS.map((step, idx) => {
              const isActive = currentStep === idx + 1
              const isCompleted = currentStep > idx + 1
              const Icon = step.icon

              return (
                <div key={step.id} className={`flex items-center gap-4 transition-all duration-500 ${isActive || isCompleted ? 'opacity-100 translate-x-0' : 'opacity-40 translate-x-4'}`}>
                  <div className={`w-11 h-11 rounded-full border-2 flex items-center justify-center transition-colors duration-300 bg-white ${isActive ? 'border-zinc-900 text-zinc-900 scale-110 shadow-lg' : isCompleted ? 'border-emerald-500 text-emerald-500' : 'border-stone-200 text-stone-300'}`}>
                    {isCompleted ? <CheckCircle2 size={20} /> : <Icon size={20} />}
                  </div>
                  <div>
                    <p className={`font-medium text-sm ${isActive ? 'text-zinc-900' : 'text-zinc-400'}`}>{step.agent}</p>
                    <p className={`text-xs ${isActive ? 'text-stone-600' : 'text-stone-300'}`}>{step.action}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    )
  }

  if (view === 'results' && analysis) {
    const visual = analysis.visual_analysis || {}
    const mode = (analysis.analysis_mode as 'quick' | 'deep') ?? 'deep'
    const modeLabel = mode === 'quick' ? 'Quick Analyze · Gemini 2.5 Flash' : 'Deep Analyze · Gemini 2.5 Pro'
    
    return (
      <div className="min-h-screen bg-stone-50">
        <nav className="w-full py-6 px-8 flex justify-between items-center border-b border-stone-200 bg-white/80 backdrop-blur-md">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-zinc-900 rounded-full flex items-center justify-center text-white">
              <Sparkles size={16} />
            </div>
            <span className="font-serif text-xl tracking-wider font-semibold text-zinc-900">Project Aura</span>
          </div>
          <button onClick={handleReset} className="px-6 py-3 bg-zinc-900 text-white text-sm font-medium uppercase tracking-widest hover:bg-zinc-800 transition-all shadow-lg hover:shadow-xl">
            New Analysis
          </button>
        </nav>

        <div className="bg-zinc-900 text-white py-12 px-6 md:px-12 mb-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-center gap-2 mb-4 text-emerald-400 text-xs font-bold tracking-widest uppercase">
              <Sparkles size={14} />
              <span>Report Generated · {modeLabel}</span>
            </div>
            <h1 className="font-serif text-3xl md:text-4xl mb-2">The Curator&apos;s Edit</h1>
            <p className="text-zinc-400 font-light max-w-xl text-sm leading-relaxed">
              Based on your goal: &quot;<span className="italic text-white">{query || 'Style improvement'}</span>&quot;
            </p>
          </div>
        </div>

        <main className="max-w-7xl mx-auto px-6 pb-20 grid lg:grid-cols-12 gap-8">
          <div className="lg:col-span-5 space-y-4">
            <div className="bg-white p-2 shadow-lg">
              <div className="grid grid-cols-2 gap-2">
                <div className="relative aspect-[3/4] bg-stone-100 overflow-hidden">
                  {preview && <img src={preview} alt="Original" className="w-full h-full object-cover" />}
                  <div className="absolute bottom-2 left-2 bg-black/60 backdrop-blur px-2 py-1 text-white text-xs font-medium">Original</div>
                </div>
                <div className="relative aspect-[3/4] bg-stone-100 overflow-hidden">
                  {analysis.generated_image_url ? (
                    <img src={analysis.generated_image_url} alt="Generated" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-stone-400 text-sm">No image generated</div>
                  )}
                  <div className="absolute bottom-2 left-2 bg-black/60 backdrop-blur px-2 py-1 text-white text-xs font-medium">Suggestion</div>
                </div>
              </div>
            </div>
          </div>

          <div className="lg:col-span-7 space-y-8">
            <section className="bg-white p-8 shadow-sm border border-stone-100">
              <div className="flex items-center gap-2 mb-6 text-zinc-400">
                <ScanLine size={16} />
                <h3 className="text-xs font-bold tracking-widest uppercase">Style Advisor Analysis</h3>
              </div>
              <div className="prose prose-stone max-w-none">
                <div className="text-zinc-700 leading-7 whitespace-pre-wrap">{analysis.final_report || 'No advice generated.'}</div>
              </div>
            </section>

            <div className="grid md:grid-cols-2 gap-6">
              <section className="bg-zinc-900 text-white p-8 shadow-lg relative overflow-hidden">
                <div className="absolute top-0 right-0 p-20 bg-gradient-to-br from-zinc-800 to-transparent rounded-bl-full opacity-50"></div>
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-6">
                    <TrendingUp size={16} className="text-emerald-400" />
                    <h3 className="text-xs font-bold tracking-widest uppercase text-emerald-400">Trend Context</h3>
                  </div>
                  <div className="prose prose-invert prose-sm max-w-none">
                    <div className="text-white/90 leading-7 space-y-3 [&>p]:my-0 [&>strong]:text-white [&>strong]:font-semibold [&>strong]:block [&>strong]:mt-4 [&>strong]:mb-2 [&>strong]:first:mt-0">
                      <div dangerouslySetInnerHTML={{ 
                        __html: (analysis.trend_summary || 'No trend data available.')
                          .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
                          .replace(/\*/g, '')
                          .replace(/\n\n/g, '</p><p>')
                          .replace(/\n/g, '<br/>')
                      }} />
                    </div>
                  </div>
                </div>
              </section>

              <section className="bg-white p-8 shadow-sm border border-stone-100">
                <div className="flex items-center gap-2 mb-6 text-zinc-400">
                  <Cpu size={16} />
                  <h3 className="text-xs font-bold tracking-widest uppercase">Visual Features</h3>
                </div>
                <div className="space-y-6">
                  {visual.gender_style && (
                    <div>
                      <div className="text-xs font-bold tracking-wider uppercase text-stone-400 mb-2">Gender Style</div>
                      <div className="text-sm text-zinc-900 leading-relaxed capitalize">{visual.gender_style}</div>
                    </div>
                  )}
                  {visual.cut && (
                    <div className="border-t border-stone-100 pt-4">
                      <div className="text-xs font-bold tracking-wider uppercase text-stone-400 mb-2">Cut & Silhouette</div>
                      <div className="text-sm text-zinc-700 leading-relaxed">{visual.cut}</div>
                    </div>
                  )}
                  {visual.color && (
                    <div className="border-t border-stone-100 pt-4">
                      <div className="text-xs font-bold tracking-wider uppercase text-stone-400 mb-2">Color Palette</div>
                      <div className="text-sm text-zinc-700 leading-relaxed">{visual.color}</div>
                    </div>
                  )}
                  {visual.fabric && (
                    <div className="border-t border-stone-100 pt-4">
                      <div className="text-xs font-bold tracking-wider uppercase text-stone-400 mb-2">Textile & Texture</div>
                      <div className="text-sm text-zinc-700 leading-relaxed">{visual.fabric}</div>
                    </div>
                  )}
                  {visual.occasion && (
                    <div className="border-t border-stone-100 pt-4">
                      <div className="text-xs font-bold tracking-wider uppercase text-stone-400 mb-2">Occasion</div>
                      <div className="text-sm text-zinc-700 leading-relaxed capitalize">{visual.occasion}</div>
                    </div>
                  )}
                </div>
              </section>
            </div>

            {analysis.image_generation_error && (
              <section className="bg-amber-50 border border-amber-200 p-6 rounded-lg">
                <p className="text-sm text-amber-800"><strong>Image Generation:</strong> {analysis.image_generation_error}</p>
              </section>
            )}
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-stone-50">
      <nav className="w-full py-6 px-8 flex justify-between items-center border-b border-stone-200 bg-white/80 backdrop-blur-md">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-zinc-900 rounded-full flex items-center justify-center text-white">
            <Sparkles size={16} />
          </div>
          <span className="font-serif text-xl tracking-wider font-semibold text-zinc-900">Project Aura</span>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-12 grid md:grid-cols-2 gap-16 items-center">
        <div className="space-y-8">
          <div className="space-y-4">
            <span className="px-3 py-1 border border-zinc-200 rounded-full text-xs font-medium tracking-widest uppercase text-stone-500 bg-stone-50">AI Supervisor Active</span>
            <h1 className="font-serif text-5xl md:text-6xl text-zinc-900 leading-[1.1]">
              Elevate your <br/>
              <span className="italic text-stone-500">visual narrative.</span>
            </h1>
            <p className="text-lg text-stone-600 font-light leading-relaxed max-w-md">
              Upload your current ensemble. Our multi-agent system analyzes trends, fit, and context to curate your perfect evolution.
            </p>
          </div>

          <div className="space-y-4">
            <label className="text-xs font-bold tracking-widest uppercase text-zinc-400">Your Scenario / Goal</label>
            <div className="relative group">
              <textarea 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="E.g., I want to look more professional for work meetings..." 
                className="w-full bg-white border border-stone-200 p-6 text-zinc-700 placeholder-zinc-300 focus:outline-none focus:border-zinc-900 transition-all resize-none h-32 shadow-sm"
              />
              <div className="absolute bottom-4 right-4">
                <Search size={16} className="text-zinc-300" />
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <button 
              onClick={() => handleAnalyze('quick')}
              disabled={!file}
              className={`group w-full py-4 px-6 border-2 flex items-center justify-between transition-all ${!file ? 'opacity-50 cursor-not-allowed border-stone-200' : 'border-emerald-500 hover:bg-emerald-50'}`}
            >
              <div className="text-left">
                <div className="tracking-widest uppercase text-xs font-bold text-zinc-900">Quick Analyze</div>
                <div className="text-xs text-stone-500">Gemini 2.5 Flash · Fast insights</div>
              </div>
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform text-emerald-600" />
            </button>
            <button 
              onClick={() => handleAnalyze('deep')}
              disabled={!file}
              className={`group w-full py-4 px-6 bg-zinc-900 text-white flex items-center justify-between transition-all hover:bg-zinc-800 ${!file ? 'opacity-50 cursor-not-allowed' : 'shadow-xl'}`}
            >
              <div className="text-left">
                <div className="tracking-widest uppercase text-xs font-bold">Deep Analyze</div>
                <div className="text-xs text-zinc-400">Gemini 2.5 Pro · Deep search</div>
              </div>
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </button>
          </div>

          {error && (
            <div className="p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 text-sm">
              {error}
            </div>
          )}
        </div>

        <div 
          className="relative aspect-[3/4] border-2 border-dashed transition-all duration-300 flex flex-col items-center justify-center cursor-pointer group overflow-hidden bg-stone-50 hover:border-zinc-400"
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          {preview ? (
            <>
              <img src={preview} alt="Upload" className="absolute inset-0 w-full h-full object-cover" />
              <div className="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
                <button className="px-6 py-2 bg-white text-black text-xs uppercase tracking-widest font-bold hover:bg-stone-100">Change Image</button>
              </div>
            </>
          ) : (
            <div className="text-center space-y-4 p-8">
              <div className="w-16 h-16 rounded-full bg-white shadow-sm flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-500">
                <Upload size={24} className="text-zinc-400 group-hover:text-zinc-900 transition-colors" />
              </div>
              <div>
                <p className="font-serif text-xl text-zinc-900">Upload Outfit</p>
                <p className="text-zinc-400 text-sm mt-1 font-light">Drag & drop or click to browse</p>
              </div>
            </div>
          )}
          <input 
            id="file-input"
            type="file" 
            className="hidden" 
            accept="image/*"
            onChange={(e) => {
              const selectedFile = e.target.files?.[0]
              if (selectedFile) handleFileSelect(selectedFile)
            }}
          />
        </div>
      </main>
    </div>
  )
}
