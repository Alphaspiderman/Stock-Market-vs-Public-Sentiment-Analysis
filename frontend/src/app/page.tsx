import { SentimentChart } from "@/components/SentimentChart";

export default function Home() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <SentimentChart />
    </div>
  );
}
