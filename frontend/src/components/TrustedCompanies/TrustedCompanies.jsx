import "./TrustedCompanies.css";

import google from "../../assets/images/logos/google.png";
import microsoft from "../../assets/images/logos/microsoft.png";
import amazon from "../../assets/images/logos/amazon.png";
import meta from "../../assets/images/logos/meta.png";
import oracle from "../../assets/images/logos/oracle.png";
import ibm from "../../assets/images/logos/ibm.png";
import infosys from "../../assets/images/logos/infosys.png";
import tcs from "../../assets/images/logos/tcs.png";
import accenture from "../../assets/images/logos/accenture.png";
import deloitte from "../../assets/images/logos/deloitte.png";
import nvidia from "../../assets/images/logos/nvidia.png";
import wipro from "../../assets/images/logos/wipro.png";

const companies = [
  {
    name: "Google",
    logo: google
  },
  {
    name: "Microsoft",
    logo: microsoft
  },
  {
    name: "Amazon",
    logo: amazon
  },
  {
    name: "Meta",
    logo: meta
  },
  {
    name: "Oracle",
    logo: oracle
  },
  {
    name: "IBM",
    logo: ibm
  },
  {
    name: "Infosys",
    logo: infosys
  },
  {
    name: "TCS",
    logo: tcs
  },
  {
    name: "Accenture",
    logo: accenture
  },
  {
    name: "Deloitte",
    logo: deloitte
  },
  {
    name: "NVIDIA",
    logo: nvidia
  },
  {
    name: "Wipro",
    logo: wipro
  }
];

function TrustedCompanies() {
  const repeatedCompanies = [
    ...companies,
    ...companies
  ];

  return (
    <section
      className="trusted"
      aria-labelledby="trusted-heading"
    >
      <div className="container trusted-container">
        <div className="trusted-header">
          <span className="trusted-badge">
            Trusted Career Preparation
          </span>

          <h2
            id="trusted-heading"
            className="trusted-heading"
          >
            Preparing students for leading companies
          </h2>

          <p className="trusted-text">
            CareerCompass helps students improve their resumes,
            understand industry expectations and prepare for
            opportunities at leading technology companies.
          </p>
        </div>

        <div className="logo-slider">
          <div className="logo-slider-fade logo-slider-fade-left" />
          <div className="logo-slider-fade logo-slider-fade-right" />

          <div className="logo-track">
            {repeatedCompanies.map(
              (company, index) => (
                <div
                  className="logo-card"
                  key={`${company.name}-${index}`}
                  title={company.name}
                >
                  <img
                    src={company.logo}
                    alt={`${company.name} logo`}
                    loading="lazy"
                  />
                </div>
              )
            )}
          </div>
        </div>

        <p className="trusted-note">
          Company logos are shown for career-preparation reference.
        </p>
      </div>
    </section>
  );
}

export default TrustedCompanies;