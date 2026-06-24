export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Dentarium AI Enterprise
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Plataforma SaaS de Inteligência Artificial Empresarial
          </p>
          <p className="text-sm text-gray-500">
            Criado por <span className="font-semibold">Roberto Ribeiro</span>
          </p>
          <p className="text-sm text-gray-500">
            GitHub: <a href="https://github.com/Username9898" className="font-semibold">@Username9898</a>
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          <FeatureCard
            title="Dashboards Automáticos"
            description="Geração inteligente de painéis com KPIs e gráficos em tempo real"
            icon="📊"
          />
          <FeatureCard
            title="OCR Inteligente"
            description="Extração de dados de PDFs, imagens e documentos escaneados"
            icon="🔍"
          />
          <FeatureCard
            title="Planilhas Autônomas"
            description="Preenchimento automático e correção de inconsistências"
            icon="📋"
          />
          <FeatureCard
            title="CAD/CAM AI"
            description="Processamento de modelos 3D para próteses dentárias"
            icon="🦷"
          />
          <FeatureCard
            title="Redução de Desperdício"
            description="Detecção de material desperdiçado e otimização de processos"
            icon="♻️"
          />
          <FeatureCard
            title="Auto-Cura"
            description="Monitoramento e recuperação automática de serviços"
            icon="🏥"
          />
        </div>

        {/* Tech Stack */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl font-bold text-center mb-8">
            Stack Tecnológico
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <TechBadge name="Python 3.11+" />
            <TechBadge name="FastAPI" />
            <TechBadge name="Next.js 14" />
            <TechBadge name="PostgreSQL" />
            <TechBadge name="Docker" />
            <TechBadge name="Kubernetes" />
            <TechBadge name="Redis" />
            <TechBadge name="MinIO" />
            <TechBadge name="Prometheus" />
            <TechBadge name="Grafana" />
            <TechBadge name="Ollama" />
            <TechBadge name="Tesseract OCR" />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-600">
          <p>© 2024 Roberto Ribeiro. Todos os direitos reservados.</p>
          <p className="text-sm mt-2">
            Licença Proprietária - Uso comercial sujeito a contrato
          </p>
        </footer>
      </div>
    </main>
  );
}

function FeatureCard({
  title,
  description,
  icon,
}: {
  title: string;
  description: string;
  icon: string;
}) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function TechBadge({ name }: { name: string }) {
  return (
    <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium">
      {name}
    </div>
  );
}