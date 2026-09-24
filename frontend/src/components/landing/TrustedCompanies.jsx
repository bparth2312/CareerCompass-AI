import google from "../../assets/images/logos/google.png";
import microsoft from "../../assets/images/logos/microsoft.png";
import amazon from "../../assets/images/logos/amazon.png";
import ibm from "../../assets/images/logos/ibm.png";
import tcs from "../../assets/images/logos/tcs.png";
import infosys from "../../assets/images/logos/infosys.png";
import accenture from "../../assets/images/logos/accenture.png";
import meta from "../../assets/images/logos/meta.png";
import oracle from "../../assets/images/logos/oracle.png";
import nvidia from "../../assets/images/logos/nvidia.png";
import deloitte from "../../assets/images/logos/deloitte.png";
import wipro from "../../assets/images/logos/wipro.png";

const companies = [
  { name: "Google", logo: google },
  { name: "Microsoft", logo: microsoft },
  { name: "Amazon", logo: amazon },
  { name: "IBM", logo: ibm },
  { name: "Meta", logo: meta },
  { name: "Oracle", logo: oracle },
  { name: "NVIDIA", logo: nvidia },
  { name: "TCS", logo: tcs },
  { name: "Infosys", logo: infosys },
  { name: "Accenture", logo: accenture },
  { name: "Deloitte", logo: deloitte },
  { name: "Wipro", logo: wipro },
];

function TrustedCompanies() {
  return (
    <section className="py-20 bg-slate-950 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-6">

        <p className="text-center text-slate-400 uppercase tracking-widest mb-12">
          Trusted Technologies & Industry Leaders
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">

          {companies.map((company) => (
            <div
              key={company.name}
              className="bg-slate-900 border border-slate-800 rounded-2xl h-28 flex items-center justify-center hover:border-indigo-500 hover:shadow-lg hover:shadow-indigo-500/20 transition-all duration-300"
            >
              <img
                src={company.logo}
                alt={company.name}
                className="max-h-12 object-contain"
              />
            </div>
          ))}

        </div>
      </div>
    </section>
  );
}

export default TrustedCompanies;