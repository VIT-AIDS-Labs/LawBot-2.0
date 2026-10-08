// frontend/lawlens.js
// Unified JavaScript for LawBot 2.0
// Handles: Legal Q&A, Document Analysis, Lawyer Connect, Evaluation

(function () {
  "use strict";

  const API_BASE = "";  // Same origin

  // =============================================
  // UTILITY FUNCTIONS
  // =============================================

  function show(el) {
    if (el) el.style.display = "";
  }

  function hide(el) {
    if (el) el.style.display = "none";
  }

  function setText(el, text) {
    if (el) el.textContent = text;
  }

  function setHTML(el, html) {
    if (el) el.innerHTML = html;
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function formatText(text) {
    // Convert newlines to paragraphs and preserve formatting
    if (!text) return "";
    return text
      .split(/\n\n+/)
      .map(function (p) { return "<p>" + escapeHtml(p.trim()).replace(/\n/g, "<br>") + "</p>"; })
      .join("");
  }

  function confidenceClass(conf) {
    if (conf === "High") return "confidence-high";
    if (conf === "Medium") return "confidence-medium";
    return "confidence-low";
  }

  function importanceClass(imp) {
    if (imp === "High") return "badge-danger";
    if (imp === "Medium") return "badge-warning";
    return "badge-info";
  }

  // =============================================
  // LEGAL Q&A PAGE
  // =============================================

  function initLegalQA() {
    var submitBtn = document.getElementById("submitQuery");
    var queryInput = document.getElementById("queryInput");
    if (!submitBtn || !queryInput) return;

    submitBtn.addEventListener("click", function () {
      submitLegalQuery();
    });

    queryInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.ctrlKey) {
        e.preventDefault();
        submitLegalQuery();
      }
    });
  }

  function submitLegalQuery() {
    var queryInput = document.getElementById("queryInput");
    var loading = document.getElementById("queryLoading");
    var resultsSection = document.getElementById("resultsSection");
    var noResults = document.getElementById("noResults");
    var errorMessage = document.getElementById("errorMessage");
    var submitBtn = document.getElementById("submitQuery");

    var query = (queryInput.value || "").trim();
    if (!query) return;

    // Reset UI
    hide(resultsSection);
    hide(noResults);
    hide(errorMessage);
    loading.style.display = "flex";
    submitBtn.disabled = true;

    fetch(API_BASE + "/legal/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query }),
    })
      .then(function (res) {
        if (!res.ok) throw new Error("Server error: " + res.status);
        return res.json();
      })
      .then(function (data) {
        hide(loading);
        submitBtn.disabled = false;

        if (!data.references || data.references.length === 0) {
          show(noResults);
          return;
        }

        // Show answer
        var answerText = document.getElementById("answerText");
        setHTML(answerText, formatText(data.answer));

        // Show references
        var refList = document.getElementById("referencesList");
        refList.innerHTML = "";

        data.references.forEach(function (ref, i) {
          var card = document.createElement("div");
          card.className = "card";
          card.style.marginBottom = "1rem";

          var sectionLabel = ref.section || ref.section_code || "Unknown";
          var actLabel = ref.act || "Indian Penal Code";
          var titleLabel = ref.title ? " — " + escapeHtml(ref.title) : "";
          var legalText = ref.legal_text
            ? '<div style="margin-top: 0.75rem; padding: 0.75rem; background: #f8f9fa; border-left: 3px solid var(--primary); border-radius: 4px; font-size: 0.9rem; color: var(--text);">' +
              "<strong>Legal Provision:</strong> " +
              escapeHtml(ref.legal_text) +
              "</div>"
            : "";
          var factPattern =
            '<div style="margin-top: 0.75rem; font-size: 0.9rem; color: var(--text-muted);">' +
            "<strong>Related Fact Pattern:</strong> " +
            escapeHtml(ref.text) +
            "</div>";

          card.innerHTML =
            '<div class="card-body">' +
            '<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">' +
            '<div>' +
            '<span class="badge badge-primary" style="font-size: 0.85rem;">Section ' +
            escapeHtml(sectionLabel) +
            "</span>" +
            '<span style="margin-left: 0.5rem; color: var(--text-muted); font-size: 0.9rem;">' +
            escapeHtml(actLabel) +
            escapeHtml(titleLabel) +
            "</span>" +
            "</div>" +
            '<div style="display: flex; gap: 0.5rem; align-items: center;">' +
            '<span class="badge ' +
            confidenceClass(ref.confidence) +
            '">' +
            escapeHtml(ref.confidence) +
            " Confidence</span>" +
            '<span style="font-size: 0.8rem; color: var(--text-muted);">Score: ' +
            (ref.score ? ref.score.toFixed(4) : "N/A") +
            "</span>" +
            "</div>" +
            "</div>" +
            legalText +
            factPattern +
            "</div>";

          refList.appendChild(card);
        });

        show(resultsSection);
      })
      .catch(function (err) {
        console.error(err);
        hide(loading);
        submitBtn.disabled = false;
        var errorText = document.getElementById("errorText");
        setText(
          errorText,
          "Something went wrong while processing your question. Please try again. (" +
            err.message +
            ")"
        );
        show(errorMessage);
      });
  }

  // =============================================
  // DOCUMENT ANALYSIS PAGE
  // =============================================

  function initDocumentAnalysis() {
    var uploadArea = document.getElementById("uploadArea");
    var fileInput = document.getElementById("fileInput");
    var uploadBtn = document.getElementById("uploadBtn");
    var fileNameEl = document.getElementById("fileName");

    if (!uploadArea || !fileInput) return;

    // Drag and drop
    uploadArea.addEventListener("dragover", function (e) {
      e.preventDefault();
      uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", function () {
      uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", function (e) {
      e.preventDefault();
      uploadArea.classList.remove("dragover");
      if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelect();
      }
    });

    fileInput.addEventListener("change", function () {
      handleFileSelect();
    });

    if (uploadBtn) {
      uploadBtn.addEventListener("click", function () {
        uploadDocument();
      });
    }

    function handleFileSelect() {
      var file = fileInput.files[0];
      if (!file) return;

      if (!file.name.toLowerCase().endsWith(".pdf")) {
        alert("Please select a PDF file.");
        fileInput.value = "";
        return;
      }

      if (fileNameEl) {
        fileNameEl.textContent = file.name + " (" + (file.size / 1024).toFixed(1) + " KB)";
        show(fileNameEl);
      }

      if (uploadBtn) uploadBtn.disabled = false;
    }
  }

  function uploadDocument() {
    var fileInput = document.getElementById("fileInput");
    var loading = document.getElementById("analysisLoading");
    var results = document.getElementById("analysisResults");
    var uploadBtn = document.getElementById("uploadBtn");

    var file = fileInput.files[0];
    if (!file) return;

    hide(results);
    show(loading);
    if (uploadBtn) uploadBtn.disabled = true;

    var formData = new FormData();
    formData.append("file", file);

    fetch(API_BASE + "/documents/analyze", {
      method: "POST",
      body: formData,
    })
      .then(function (res) {
        if (!res.ok) {
          return res.json().then(function (data) {
            throw new Error(data.detail || "Server error: " + res.status);
          });
        }
        return res.json();
      })
      .then(function (data) {
        hide(loading);
        if (uploadBtn) uploadBtn.disabled = false;

        // Populate results
        var docName = document.getElementById("docName");
        var docPages = document.getElementById("docPages");
        var docSummary = document.getElementById("docSummary");
        var clausesList = document.getElementById("clausesList");
        var docMetadata = document.getElementById("docMetadata");

        if (docName) setText(docName, data.filename || "Unknown");
        if (docPages) setText(docPages, (data.page_count || 0) + " pages");
        if (docSummary) setHTML(docSummary, formatText(data.summary));

        // Clauses
        if (clausesList) {
          clausesList.innerHTML = "";
          if (data.clauses && data.clauses.length > 0) {
            data.clauses.forEach(function (clause) {
              var clauseCard = document.createElement("div");
              clauseCard.className = "card";
              clauseCard.style.marginBottom = "0.75rem";
              clauseCard.innerHTML =
                '<div class="card-body">' +
                '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">' +
                "<strong>" +
                escapeHtml(clause.title || "Clause") +
                "</strong>" +
                '<span class="badge ' +
                importanceClass(clause.importance) +
                '">' +
                escapeHtml(clause.importance || "Medium") +
                "</span>" +
                "</div>" +
                '<p style="margin: 0; font-size: 0.9rem; color: var(--text-muted);">' +
                escapeHtml(clause.content || "") +
                "</p>" +
                "</div>";
              clausesList.appendChild(clauseCard);
            });
          } else {
            clausesList.innerHTML =
              '<p class="text-muted">No specific clauses identified.</p>';
          }
        }

        // Metadata
        if (docMetadata && data.metadata) {
          var metaHtml = "";
          var metaMap = {
            document_type: "Document Type",
            parties: "Parties",
            key_dates: "Key Dates",
            jurisdiction: "Jurisdiction",
          };
          for (var key in metaMap) {
            if (data.metadata[key]) {
              metaHtml +=
                '<div style="margin-bottom: 0.5rem;">' +
                "<strong>" +
                metaMap[key] +
                ":</strong> " +
                escapeHtml(data.metadata[key]) +
                "</div>";
            }
          }
          docMetadata.innerHTML = metaHtml || '<p class="text-muted">No additional metadata extracted.</p>';
        }

        show(results);
      })
      .catch(function (err) {
        console.error(err);
        hide(loading);
        if (uploadBtn) uploadBtn.disabled = false;
        alert("Error analyzing document: " + err.message);
      });
  }

  // =============================================
  // LAWYER CONNECT PAGE
  // =============================================

  var allLawyers = [];

  function initLawyerConnect() {
    var searchBtn = document.getElementById("searchLawyers");
    if (!searchBtn) return;

    // Load filters and lawyers
    loadFilters();
    loadLawyers();

    searchBtn.addEventListener("click", function () {
      loadLawyers();
    });

    // Reset button
    var resetBtn = document.getElementById("resetFilters");
    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        var specFilter = document.getElementById("filterSpecialization");
        var locFilter = document.getElementById("filterLocation");
        var langFilter = document.getElementById("filterLanguage");
        if (specFilter) specFilter.value = "";
        if (locFilter) locFilter.value = "";
        if (langFilter) langFilter.value = "";
        loadLawyers();
      });
    }
  }

  function loadFilters() {
    fetch(API_BASE + "/lawyers/filters")
      .then(function (res) { return res.json(); })
      .then(function (data) {
        populateSelect("filterSpecialization", data.specializations, "All Specializations");
        populateSelect("filterLocation", data.locations, "All Locations");
        populateSelect("filterLanguage", data.languages, "All Languages");
      })
      .catch(function (err) {
        console.error("Error loading filters:", err);
      });
  }

  function populateSelect(id, options, defaultLabel) {
    var sel = document.getElementById(id);
    if (!sel) return;

    // Keep the default option
    sel.innerHTML = '<option value="">' + defaultLabel + "</option>";
    if (options) {
      options.forEach(function (opt) {
        var o = document.createElement("option");
        o.value = opt;
        o.textContent = opt;
        sel.appendChild(o);
      });
    }
  }

  function loadLawyers() {
    var specFilter = document.getElementById("filterSpecialization");
    var locFilter = document.getElementById("filterLocation");
    var langFilter = document.getElementById("filterLanguage");

    var params = new URLSearchParams();
    if (specFilter && specFilter.value) params.append("specialization", specFilter.value);
    if (locFilter && locFilter.value) params.append("location", locFilter.value);
    if (langFilter && langFilter.value) params.append("language", langFilter.value);

    var url = API_BASE + "/lawyers" + (params.toString() ? "?" + params.toString() : "");

    fetch(url)
      .then(function (res) { return res.json(); })
      .then(function (data) {
        allLawyers = data.lawyers || [];
        renderLawyers(allLawyers);
      })
      .catch(function (err) {
        console.error("Error loading lawyers:", err);
      });
  }

  function renderLawyers(lawyers) {
    var grid = document.getElementById("lawyerGrid");
    var countEl = document.getElementById("lawyerCount");

    if (!grid) return;
    grid.innerHTML = "";

    if (countEl) {
      setText(countEl, lawyers.length + " lawyer" + (lawyers.length !== 1 ? "s" : "") + " found");
    }

    if (lawyers.length === 0) {
      grid.innerHTML =
        '<div class="empty-state" style="grid-column: 1 / -1;">' +
        "<h3>No lawyers found</h3>" +
        "<p>Try adjusting your filters.</p>" +
        "</div>";
      return;
    }

    lawyers.forEach(function (l) {
      var initials = l.name
        .split(" ")
        .filter(function (w) { return w.length > 0 && w[0] === w[0].toUpperCase() && w !== "Adv."; })
        .map(function (w) { return w[0]; })
        .join("")
        .substring(0, 2);

      var card = document.createElement("div");
      card.className = "card card-interactive";
      card.innerHTML =
        '<div class="card-body">' +
        '<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">' +
        '<div style="width: 52px; height: 52px; border-radius: 50%; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; flex-shrink: 0;">' +
        escapeHtml(initials) +
        "</div>" +
        "<div>" +
        '<h3 style="margin: 0; font-size: 1.05rem;">' +
        escapeHtml(l.name) +
        "</h3>" +
        '<span class="badge badge-accent" style="margin-top: 4px; display: inline-block;">' +
        escapeHtml(l.specialization) +
        "</span>" +
        "</div>" +
        "</div>" +
        '<div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.5rem;">' +
        escapeHtml(l.location) +
        "</div>" +
        '<div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.5rem;">' +
        escapeHtml(l.experience_years) +
        " years experience" +
        "</div>" +
        '<div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">' +
        "Languages: " +
        escapeHtml(l.languages) +
        "</div>" +
        '<button class="btn btn-secondary btn-sm" onclick="showLawyerProfile(' +
        l.id +
        ')">View Profile</button>' +
        "</div>";

      grid.appendChild(card);
    });
  }

  // Make showLawyerProfile global
  window.showLawyerProfile = function (id) {
    fetch(API_BASE + "/lawyers/" + id)
      .then(function (res) { return res.json(); })
      .then(function (lawyer) {
        var modal = document.getElementById("lawyerModal");
        if (!modal) return;

        var initials = lawyer.name
          .split(" ")
          .filter(function (w) { return w.length > 0 && w[0] === w[0].toUpperCase() && w !== "Adv."; })
          .map(function (w) { return w[0]; })
          .join("")
          .substring(0, 2);

        var availClass = lawyer.availability === "Available" ? "badge-success" : "badge-warning";

        var content = document.getElementById("lawyerModalContent");
        if (content) {
          content.innerHTML =
            '<div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 1.5rem;">' +
            '<div style="width: 64px; height: 64px; border-radius: 50%; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.3rem; flex-shrink: 0;">' +
            escapeHtml(initials) +
            "</div>" +
            "<div>" +
            '<h2 style="margin: 0;">' +
            escapeHtml(lawyer.name) +
            "</h2>" +
            '<span class="badge badge-accent">' +
            escapeHtml(lawyer.specialization) +
            "</span> " +
            '<span class="badge ' +
            availClass +
            '">' +
            escapeHtml(lawyer.availability) +
            "</span>" +
            "</div>" +
            "</div>" +
            '<div class="grid-2" style="gap: 1rem; margin-bottom: 1.5rem;">' +
            '<div><strong>Experience:</strong> ' +
            lawyer.experience_years +
            " years</div>" +
            "<div><strong>Location:</strong> " +
            escapeHtml(lawyer.location) +
            "</div>" +
            "<div><strong>Languages:</strong> " +
            escapeHtml(lawyer.languages) +
            "</div>" +
            "<div><strong>Contact:</strong> " +
            escapeHtml(lawyer.contact) +
            "</div>" +
            "</div>" +
            "<h3>About</h3>" +
            '<p style="line-height: 1.7; color: var(--text-muted);">' +
            escapeHtml(lawyer.profile) +
            "</p>" +
            '<button class="btn btn-primary" style="margin-top: 1rem;" onclick="openConsultationForm(' +
            lawyer.id +
            ", '" +
            escapeHtml(lawyer.name).replace(/'/g, "\\'") +
            "')\">" +
            "Request Consultation" +
            "</button>";
        }

        show(modal);
      })
      .catch(function (err) {
        console.error("Error loading lawyer profile:", err);
      });
  };

  // Make openConsultationForm global
  window.openConsultationForm = function (lawyerId, lawyerName) {
    var lawyerModal = document.getElementById("lawyerModal");
    var consultModal = document.getElementById("consultationModal");
    var lawyerIdField = document.getElementById("consultationLawyerId");
    var lawyerNameField = document.getElementById("consultationLawyerName");

    hide(lawyerModal);

    if (lawyerIdField) lawyerIdField.value = lawyerId;
    if (lawyerNameField) setText(lawyerNameField, lawyerName);

    show(consultModal);
  };

  function initConsultationForm() {
    var submitBtn = document.getElementById("submitConsultationBtn");
    var cancelBtn = document.getElementById("cancelConsultationBtn");
    var consultModal = document.getElementById("consultationModal");

    if (submitBtn) {
      submitBtn.addEventListener("click", function () {
        submitConsultation();
      });
    }

    if (cancelBtn) {
      cancelBtn.addEventListener("click", function () {
        hide(consultModal);
      });
    }

    // Close modals on overlay click
    var lawyerModal = document.getElementById("lawyerModal");
    if (lawyerModal) {
      lawyerModal.addEventListener("click", function (e) {
        if (e.target === lawyerModal) hide(lawyerModal);
      });
    }

    if (consultModal) {
      consultModal.addEventListener("click", function (e) {
        if (e.target === consultModal) hide(consultModal);
      });
    }

    // Close buttons
    document.querySelectorAll("[data-close-modal]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var target = document.getElementById(btn.getAttribute("data-close-modal"));
        if (target) hide(target);
      });
    });
  }

  function submitConsultation() {
    var name = document.getElementById("consultationName");
    var issue = document.getElementById("consultationLegalIssue");
    var lang = document.getElementById("consultationLanguage");
    var date = document.getElementById("consultationDate");
    var contact = document.getElementById("consultationContact");
    var desc = document.getElementById("consultationDescription");
    var lawyerId = document.getElementById("consultationLawyerId");
    var consultModal = document.getElementById("consultationModal");
    var successEl = document.getElementById("consultationSuccess");

    if (!name || !name.value.trim()) { alert("Please enter your name."); return; }
    if (!issue || !issue.value.trim()) { alert("Please describe the legal issue."); return; }
    if (!contact || !contact.value.trim()) { alert("Please provide contact information."); return; }

    var data = {
      name: name.value.trim(),
      legal_issue: issue.value.trim(),
      preferred_language: lang ? lang.value : "",
      preferred_date: date ? date.value : "",
      contact_info: contact.value.trim(),
      description: desc ? desc.value.trim() : "",
      lawyer_id: lawyerId ? parseInt(lawyerId.value) : null,
    };

    fetch(API_BASE + "/consultations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then(function (res) { return res.json(); })
      .then(function (result) {
        hide(consultModal);

        if (successEl) {
          successEl.innerHTML =
            '<div class="alert alert-success">' +
            "<strong>Consultation request submitted successfully.</strong> " +
            "Your request ID is #" +
            result.id +
            ". The lawyer will contact you soon." +
            "</div>";
          show(successEl);

          setTimeout(function () {
            hide(successEl);
          }, 8000);
        }

        // Reset form
        if (name) name.value = "";
        if (issue) issue.value = "";
        if (lang) lang.value = "";
        if (date) date.value = "";
        if (contact) contact.value = "";
        if (desc) desc.value = "";
      })
      .catch(function (err) {
        console.error("Error submitting consultation:", err);
        alert("Error submitting consultation request. Please try again.");
      });
  }

  // =============================================
  // EVALUATION PAGE
  // =============================================

  function initEvaluation() {
    // The evaluation page is mostly static HTML.
    // Optionally load dynamic data from API.
    var page = document.querySelector("[data-page='evaluation']");
    if (!page) return;

    fetch(API_BASE + "/evaluation/data")
      .then(function (res) { return res.json(); })
      .then(function (data) {
        // Could update dynamic elements here if needed
        console.log("Evaluation data loaded:", data);
      })
      .catch(function (err) {
        console.log("Evaluation data endpoint not available:", err.message);
      });
  }

  // =============================================
  // INITIALIZATION
  // =============================================

  document.addEventListener("DOMContentLoaded", function () {
    var page = document.body.getAttribute("data-page");

    switch (page) {
      case "legal-qa":
        initLegalQA();
        break;
      case "document-analysis":
        initDocumentAnalysis();
        break;
      case "lawyer-connect":
        initLawyerConnect();
        initConsultationForm();
        break;
      case "evaluation":
        initEvaluation();
        break;
    }
  });
})();
