import Navbar from "../../components/layout/Navbar";
import Hero from "../../components/landing/Hero";
import TrustedCompanies from "../../components/landing/TrustedCompanies";
import Features from "../../components/landing/Features";
import HowItWorks from "../../components/landing/HowItWorks";
import Statistics from "../../components/landing/Statistics";

function LandingPage() {
  return (
    <>
      <Navbar />
      <Hero />
      <TrustedCompanies />
      <Features />
      <HowItWorks />
      <Statistics />
    </>
  );
}

export default LandingPage;